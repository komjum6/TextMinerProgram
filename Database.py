#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 08:59:29 2018

@author: huub
"""


import mysql.connector

def get_conn():
    #HARDCODED WANT HAHA CYTOSINE
    
    cnx = mysql.connector.connect(user='owe8_pg2', password='blaat1234',
                              host='127.0.0.1',
                              database='owe8_pg2',
                              use_pure=True)
    return cnx
    


def insert_pubmed(pmid,titel,publisch_year):