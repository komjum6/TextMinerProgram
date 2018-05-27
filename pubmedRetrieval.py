#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:31:14 2018

@author: huub
"""
from Bio import Entrez
import time

def search(query):
    Entrez.email = 'huub.goltstein@gmail.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='100000',
                            retmode='xml', 
                            term=query)
    time.sleep(1) #als de NCBI server druk is, kan dit fout gaan omdat het lezen gebeurt voor het zenden klaar is
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

def get_PMID(paper):
    return str(paper['MedlineCitation']['PMID'])

def get_title(paper):
    return paper['MedlineCitation']['Article']['ArticleTitle'].encode('ascii', 'ignore')

#28911628 rip
def get_abstract(paper):
    
    abstract = paper['MedlineCitation']['Article']['Abstract']
        
    text = ""
    
    if isinstance(abstract, str):
        text = abstract.encode('ascii', 'ignore')
    else:
        for a in abstract['AbstractText']:
            text += str(a.encode('ascii', 'ignore'))
            
    return text


def get_article_date(paper):
    time = paper['MedlineCitation']['DateCompleted']
    return time

def get_keywords(paper):
    
    keys = paper['MedlineCitation']['KeywordList'] 

    try: 
        key = keys[0] 
        return ' '.join(key) 
    except: 
        pass 
    