#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:31:14 2018

@author: huub
"""
from Bio import Entrez
import time

import mysql.connector

def get_conn():
    #HARDCODED WANT HAHA CYTOSINE
    
    cnx = mysql.connector.connect(user='owe8_pg1', password='blaat1234',
                              host='127.0.0.1',
                              db='owe8_pg1')
    return cnx

def search_ids(query):
    Entrez.email = 'huub.goltstein@gmail.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='0',
                            retmode='xml', 
                            term=query)
    
    
    time.sleep(1) #als de NCBI server druk is, kan dit fout gaan omdat het lezen gebeurt voor het zenden klaar is
    results = Entrez.read(handle)
    
    amount_of_hits = int(results['Count'])
    print(amount_of_hits)
    
    id_lijst = []
    
    batch_size = 10000
    
    for i in range(0,amount_of_hits,batch_size):
        Entrez.email = 'huub.goltstein@gmail.com'
        handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax=batch_size,
                            retstart=i,
                            retmode='xml', 
                            term=query)
        print("done with first up to ",i," articles")
        results = Entrez.read(handle)
        id_lijst.extend(results['IdList'])
        time.sleep(1)

    print(len(id_lijst))
    return id_lijst

def insert_term_articles(id_lijst, term, cnx):
    
    cursor = cnx.cursor()
        
    sel_query =     """
                    SELECT id FROM terms
                    WHERE mesh_term = %s         
                    """
    
    cursor.execute(sel_query,(term,))
    term_id = cursor.fetchall()[0][0]
    
    data = [(article_id.encode('utf-8'),term_id) for article_id in id_lijst]
    
    stmt = "INSERT IGNORE INTO articles_terms (articles_id, terms_id) VALUES (%s, %s)"
   
    cursor.executemany(stmt, data)
    
    
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
    
    
def insert_article(id_lijst,cnx):
    cursor = cnx.cursor()
    
    nieuw = [(int(pmid),) for pmid in id_lijst]
    
    insert_stmt = "INSERT IGNORE INTO articles (PMID) VALUES (%s)"  #nobody cares if itś there already  
    cursor.executemany(insert_stmt,nieuw)
    
    return

def searcherino(term):
    

    
    id_lijst = search_ids(term)
    
    conn = get_conn()
    
    for i in range(0,len(id_lijst),1000):
        small = id_lijst[i:i+1000]
        insert_article(small,conn)
        insert_term_articles(small,term,conn)
        print("at: ",i)
        conn.commit()
    
    
    print("aw ye boi")
    
