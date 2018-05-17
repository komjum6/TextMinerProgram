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
                           rettype='medline',
                           retmode="text",
                           webenv=search_results["WebEnv"],
                           query_key=search_results['QueryKey']
                           id=ids)
    results = handle.read()
    handle.close()
    return results

