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