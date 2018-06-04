#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:31:14 2018

@author: huub
"""
from Bio import Entrez
import time
from database import get_conn,insert_article,insert_term_articles

#Functie die alle pubmed identifiers ophaalt bij een query
#Doordat NCBI het niet fijn vindt als je tijdens werkuren teveel stress oplevert
#zitten er een paar time.sleeps(1) in, deels om NCBI te ontlasten en deels om
#op cytosine minder belastend te zijn en zo te vermijden dat je process gekilled wordt #hacks
def search_ids(query):
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


#Functie voor het vinden van alle artikelen die iets te maken hebben met de zoekterm en 
#deze op te slaan in de database, hij is voor de aanroep van een developer omdat bij het halverwege misgaan van deze functie
#door omstandigheden de database niet meer stabiel is, dit omdat het committen van zoveel veranderingen tegelijk de server voor een verlengde
#tijd unresponsive maakt en op een gedeelde server je dit niet kan maken naar de andere gebruikers toe
def search(term):
    
    id_lijst = search_ids(term)
    
    conn = get_conn()
    
    for i in range(0,len(id_lijst),1000):
        small = id_lijst[i:i+1000]
        insert_article(small,conn)
        insert_term_articles(small,term,conn)
        print("at: ",i)
        conn.commit()
      
    print("finished")