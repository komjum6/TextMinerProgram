#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:31:14 2018

@author: huub
"""
from Bio import Entrez
import time
from database import get_conn,insert_article,insert_term_articles,get_unmined_terms, set_mined_variable, get_article_pmids


#Hier staat vrij hardcoded, het domein van pubmed met daarin alle artikelen die ofwel over bitter gourd ofwel over yams gaan
#Omdat het zoeken op alle data op NCBI zeker voor termen als "sugars" veel te intensief is,
#Gaan we alleen maar het domein van de bitter gourds en yams bekijken, dit zijn in totaal 2106 artikelen en 
#Hierdoor redelijk eenvoudig te behappen, de co-occurance kan hierna bepaalt worden met SQL HOPELIJK zonder de
#mySQL database zo intens te stressen als eerst gedaan werd (excuses).
#Deze hardcode spijt me zeer, maar om de database klein te houden en toch relevant is dit nodig.
def search_domain():
    
    search_domain_string = """("momordica charantia"[MeSH Terms] OR ("momordica"[All Fields] AND "charantia"[All Fields]) OR "momordica charantia"[All Fields]) OR ("dioscorea"[MeSH Terms] OR "dioscorea"[All Fields]) """
                            
    return search_domain_string

#Functie die alle pubmed identifiers ophaalt bij een query
#Doordat NCBI het niet fijn vindt als je tijdens werkuren teveel stress oplevert
#zitten er een paar time.sleeps(1) in, deels om NCBI te ontlasten en deels om
#op cytosine minder belastend te zijn en zo te vermijden dat je process gekilled wordt #hacks
def search_ids(query):
    
    query = search_domain() + query
    
    Entrez.email = 'huub.goltstein@gmail.com'
    handle = Entrez.esearch(db='pubmed', #ophalen van de grootte van de vraag
                            sort='relevance', 
                            retmax='0',
                            retmode='xml', 
                            term=query)
    
    
    
    time.sleep(1) #als de NCBI server druk is, kan dit fout gaan omdat het lezen gebeurt voor het zenden klaar is
    results = Entrez.read(handle)
    
    amount_of_hits = int(results['Count'])
    print(amount_of_hits)
    
    id_lijst = []
    
    batch_size = 10000 #vraag de XML op in batches van 10.000 en het zijn alleen de ID's
    
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

def get_titels(id_lijst):
    
    pmid_title_list = []
    id_string_lijst = [str(i) for i in id_lijst]
    
    handle = Entrez.esummary(db="pubmed", id=",".join(id_string_lijst), retmode="xml")
    records = Entrez.parse(handle)
    for i,record in enumerate(records):
        ids = id_lijst[i]
        title = record['Title'].encode('utf-8')
        
        pmid_title_list.append((title,ids))
        
    return pmid_title_list
    

def fill_article_titles():
    conn = get_conn()
    
    pmid_list = get_article_pmids(conn)
    
    insert_list = get_titels(pmid_list)
    
    cursor = conn.cursor()
    
    update_query = """
                    UPDATE articles
                    SET title=%s
                    WHERE PMID = %s
                    """
    
    cursor.executemany(update_query,insert_list)
    conn.commit()
    print("finished inserting article titles")

#Functie voor het vinden van alle artikelen die iets te maken hebben met de zoekterm en 
#deze op te slaan in de database, hij is voor de aanroep van een developer omdat bij het halverwege misgaan van deze functie
#door omstandigheden de database niet meer stabiel is, dit omdat het committen van zoveel veranderingen tegelijk de server voor een verlengde
#tijd unresponsive maakt en op een gedeelde server je dit niet kan maken naar de andere gebruikers toe
def search():
    
    conn = get_conn()
    terms = get_unmined_terms(conn)
    
    for term in terms:
        print("doing term: ",term)
        id_lijst = search_ids(term)
        
        for i in range(0,len(id_lijst),1000):
            small = id_lijst[i:i+1000]
            insert_article(small,conn)
            insert_term_articles(small,term,conn)
            print("at: ",i)
            conn.commit()
        
        set_mined_variable(True,term,conn)
      
    conn.close()
    print("finished")