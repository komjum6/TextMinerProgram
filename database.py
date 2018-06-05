# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 17:47:33 2018

@author: Huub
"""
import mysql.connector

#het aanmaken van de connectie wordt hier gedaan, omdat dit een vrij hardcoded process is en
#misschien aangepast moet worden
def get_conn():
    #HARDCODED WANT HAHA CYTOSINE
    
    cnx = mysql.connector.connect(user='owe8_pg1', 
                                  password='blaat1234',
                                  host='127.0.0.1',
                                  db='owe8_pg1')
    return cnx

#Functie voor het inserteren van term artikel combinaties
#een lijst met id's gaat erin en een term
#en daarna worden in de database al deze termen geinserteerd
def insert_term_articles(id_lijst, term, cnx):
    
    cursor = cnx.cursor()
        
    sel_query =     """
                    SELECT id FROM terms
                    WHERE mesh_term = %s         
                    """
    
    cursor.execute(sel_query,(term,))
    term_id = cursor.fetchall()[0][0]
    
    data = [(article_id.encode('utf-8'),term_id) for article_id in id_lijst]
    
    stmt = "INSERT IGNORE INTO articles_terms (articles_id, terms_id) VALUES (%s, %s)" #insert IGNORE omdat als 4 keer je programma gekilled wordt omdat de server boos is, je gewoon wil dat hij in ieder geval iets opslaat zodat je daarna jammerlijk hardcoded verderop door kan gaan.
   
    cursor.executemany(stmt, data)
    
    
def set_mined_variable(boolean,mesh_term,cnx):
    
    update_query = """
                    UPDATE terms
                    SET finished_mining=%s
                    WHERE mesh_term = %s
                    """
    
    cursor = cnx.cursor()
    
    cursor.execute(update_query,(boolean,mesh_term))
    cnx.commit()
    cursor.close()
    

    
#vind alle termen die nog niet gemined zijn
def get_unmined_terms(cnx):
    
    
    terms = [] 
    sel_query = """
                SELECT mesh_term
                FROM terms
                WHERE finished_mining = FALSE
                """
                
    cursor = cnx.cursor()
    cursor.execute(sel_query)
    
    rows = cursor.fetchall()
    
    for row in rows:
        terms.append(row[0])
    
    cursor.close()
    return terms

def get_article_pmids(cnx):
    
    pmid_list = []
    
    sel_query = """
                SELECT PMID
                FROM articles
                WHERE title IS NULL
                """
                
    cursor = cnx.cursor()
    
    cursor.execute(sel_query)
    
    for row in cursor.fetchall():
        pmid_list.append(row[0])
        
    cursor.close()
    return pmid_list


def get_overlap_pmid_title(term1,term2,cnx):
    
    sel_query = """
                SELECT articles.PMID, articles.title
                FROM articles_terms AS at1
                INNER JOIN articles_terms AS at2 ON at1.articles_id = at2.articles_id
                INNER JOIN terms AS t1 ON at1.terms_id = t1.id
                INNER JOIN terms AS t2 ON at2.terms_id = t2.id
                INNER JOIN articles ON at1.articles_id = articles.PMID
                WHERE t1.mesh_term =  %s
                AND t2.mesh_term =  %s
                """
                
    cursor = cnx.cursor()
    cursor.execute(sel_query,(term1,term2))
    
    id_lijst = []
    
    for row in cursor.fetchall():
        id_lijst.append(row[0:2])
    
    return id_lijst
    

# het inserteren van terms in de database
# Deze functie was bedoeld om te ondersteunen dat de gebruiker dingen in de database kan inserteren voor latere verwerking
# Uiteindelijk onder andere door synoniemen en hoofdletter/kleineletter issues en andere zaken is gekozen deze functie
# niet te gebruiken om de stabiliteit te waarborgen, spijtig genoeg
def insert_term(term,term_type, cnx):
    
    cursor = cnx.cursor()
        
    sel_query = """
                SELECT id FROM term_type
                WHERE term_type = %s         
                """
                    
    cursor.execute(sel_query,term_type)
    term_type_id = cursor.fetchall()[0][0]
    
    sel_query = """
                SELECT MAX(id) FROM terms
                """
    cursor.execute(sel_query)
    term_id = int(cursor.fetchall()[0][0])+1
    
    stmt = "INSERT INTO terms (id	,mesh_term,	term_type_id) VALUES (%s,%s,%s)"
    data = (term_id, term, term_type_id)
    cursor.execute(stmt,data)
    cnx.commit()
    return
    
#het inserteren van de PUBMED Identifiers in de database,
#Het opslaan van de titels van een miljoen artikelen, 
def insert_article(id_lijst,cnx):
    cursor = cnx.cursor()
    
    nieuw = [(int(pmid),) for pmid in id_lijst]
    
    insert_stmt = "INSERT IGNORE INTO articles (PMID) VALUES (%s)"  #nobody cares if itś there already  
    cursor.executemany(insert_stmt,nieuw)
    
    return