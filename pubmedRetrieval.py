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

if __name__ == '__main__':
    results = search('Momordica charantia')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
        print(str(i) + ":"+ str(paper['MedlineCitation']['KeywordList']))
        #print(str(i) + ":"+ str(paper['MedlineCitation']['Article']['ArticleDate']))
        print(str(i) + ":"+ str(paper['MedlineCitation']['PMID']))
        #print(str(i) + ":"+ str(paper['MedlineCitation']['Article']['Abstract']))
   
