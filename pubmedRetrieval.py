#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:31:14 2018

@author: huub
"""
from Bio import Entrez

def search(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='100000',
                            retmode='xml', 
                            term=query)
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
    return str(paper['MedlineCitation']['ArticleTitle'])

def get_abstract(paper):
    
    abstract = paper['MedlineCitation']['Article']['Abstract']
        
    text = ""
    
    if isinstance(abstract, str):
        text = abstract
    else:
        for a in abstract['AbstractText']:
            text += str(a)
            
    return text


def get_article_date(paper):
    return str(paper['MedlineCitation']['Article']['ArticleDate'])

def get_keywords(paper):
    
    keys = paper['MedlineCitation']['KeywordList'] 

    try: 
        key = keys[0] 
        return ' '.join(key) 
    except: 
        pass 