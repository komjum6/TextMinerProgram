#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 08:59:29 2018

@author: huub
"""

import datetime
import mysql.connector

def get_conn():
    #HARDCODED WANT HAHA CYTOSINE
    
    cnx = mysql.connector.connect(user='owe8_pg2', password='blaat1234',
                              host='127.0.0.1',
                              database='owe8_pg2',
                              use_pure=True)
    return cnx

def insert_pubmed(pmid,titel,year,month,day, cnx):
    
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT pmid FROM pubmed WHERE pmid = %(pmid)s")
    cursor.execute(select_stmt, {'pmid' : pmid})
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        return result[0][0]
    else:

        insert_statement = ("INSERT INTO pubmed (pmid,titel, publisch_year) "
                     "VALUES (%s,%s,%s)")
        data = (pmid, titel, datetime.date(year, month, day))
    
        cursor.execute(insert_statement,data)
        cnx.commit()
        
        select_stmt = ("SELECT pmid FROM pubmed WHERE pmid = %(pmid)s")
        cursor.execute(select_stmt, {'pmid' : pmid})
        result = cursor.fetchall()
        return result[0][0]
        
        
        
    

def insert_gewas(naam, cnx):
    
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT gewas_ID FROM gewas WHERE naam = %(naam)s")
    cursor.execute(select_stmt, { 'naam': naam })
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        return result[0][0]
        
    else:        
        insert_stmt = ("INSERT INTO gewas (naam) "
                     "VALUES (%s)")
        
        cursor.execute(insert_stmt,(naam,))
        cnx.commit()
        
        select_stmt = ("SELECT gewas_ID FROM gewas WHERE naam = %(naam)s")
        cursor.execute(select_stmt, { 'naam': naam })
        result = cursor.fetchall()
        return result[0][0]
        
        
def insert_compound(naam, cnx):
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT compound_ID FROM compound WHERE naam = %(naam)s")
    cursor.execute(select_stmt, { 'naam': naam })
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        return result[0][0]
        
    else:        
        insert_stmt = ("INSERT INTO compound (naam) "
                     "VALUES (%s)")
        
        cursor.execute(insert_stmt,(naam,))
        cnx.commit()
        
        select_stmt = ("SELECT compound_ID FROM compound WHERE naam = %(naam)s")
        cursor.execute(select_stmt, { 'naam': naam })
        result = cursor.fetchall()
        return result[0][0]

    



def insert_health_factor(naam, cnx):
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT health_factor_ID FROM health_factor WHERE naam = %(naam)s")
    cursor.execute(select_stmt, { 'naam': naam })
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        return result[0][0]
        
    else:        
        insert_stmt = ("INSERT INTO health_factor (naam) "
                     "VALUES (%s)")
        
        cursor.execute(insert_stmt,(naam,))
        cnx.commit()
        
        select_stmt = ("SELECT health_factor_ID FROM health_factor WHERE naam = %(naam)s")
        cursor.execute(select_stmt, { 'naam': naam })
        result = cursor.fetchall()
        return result[0][0]

def insert_testsubject(naam,cnx):
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT testsubject_ID FROM testsubject WHERE naam = %(naam)s")
    cursor.execute(select_stmt, { 'naam': naam })
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        return result[0][0]
        
    else:        
        insert_stmt = ("INSERT INTO testsubject (naam) "
                     "VALUES (%s)")
        
        cursor.execute(insert_stmt,(naam,))
        cnx.commit()
        
        select_stmt = ("SELECT testsubject_ID FROM testsubject WHERE naam = %(naam)s")
        cursor.execute(select_stmt, { 'naam': naam })
        result = cursor.fetchall()
        return result[0][0]
     
        
    
# we gaan ervanuit dat de compound er al instaat, want dat moet eerst gebeuren
def insert_pubmed_has_compound(pmid, compound, frequency, cnx):
    
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT compound_ID FROM compound WHERE naam = %(naam)s")
    cursor.execute(select_stmt, { 'naam': compound })
    
    result = cursor.fetchall()
    
    compound_ID = result[0][0]
    
    ## check if already existant
    select_stmt = ("SELECT count(1)"
                   "FROM pubmed_has_compound "
                   "WHERE pubmed_pmid = %(pmid)s "
                   "AND compound_compound_ID = %(compound_ID)s")
    cursor.execute(select_stmt, { 'pmid': pmid, 'compound_ID' : compound_ID })
    
    exist_check = cursor.fetchall()[0][0]
    
    if exist_check < 1:
    
    
        insert_stmt = ("INSERT INTO pubmed_has_compound (pubmed_pmid, compound_compound_ID,frequency) "
                     "VALUES (%s,%s,%s)")
    
        data = (pmid, compound_ID, frequency)
    
        cursor.execute(insert_stmt,data)
        cnx.commit()
   
    
    
# we gaan ervanuit dat het gewas er al instaat, want dat moet eerst gebeuren
def insert_pubmed_has_gewas(pmid, gewas, frequency, cnx):
    
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT gewas_ID FROM gewas WHERE naam = %(naam)s")
    cursor.execute(select_stmt, { 'naam': gewas })
    
    result = cursor.fetchall()
    
    gewas_ID = result[0][0]
    
    
    ## check if already existant
    select_stmt = ("select count(1) "
                   "FROM pubmed_has_gewas "
                   "WHERE pubmed_pmid = %(pmid)s "
                   "AND gewas_gewas_ID = %(gewas_ID)s")
    cursor.execute(select_stmt, { 'pmid': pmid, 'gewas_ID' : gewas_ID })
    
    exist_check = cursor.fetchall()[0][0]
    
    if exist_check < 1:
    
    
        insert_stmt = ("INSERT INTO pubmed_has_gewas (pubmed_pmid, gewas_gewas_ID,frequency) "
                     "VALUES (%s,%s,%s)")
    
        data = (pmid, gewas_ID, frequency)
    
        cursor.execute(insert_stmt,data)
        cnx.commit()
    
    
# we gaan ervanuit dat de health_factor er al instaat want dat moet eerst gebeuren
def insert_pubmed_has_health_factor(pmid, health_factor, frequency, cnx):
    
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT health_factor_ID FROM health_factor WHERE naam = %(naam)s")
    cursor.execute(select_stmt, { 'naam': health_factor })
    
    result = cursor.fetchall()
    
    health_factor_ID = result[0][0]
    
    ## check if already existant
    select_stmt = ("SELECT count(1) "
                   "FROM pubmed_has_health_factor "
                   "WHERE pubmed_pmid = %(pmid)s "
                   "AND health_factor_health_factor_ID = %(health_factor_ID)s")
    cursor.execute(select_stmt, { 'pmid': pmid, 'health_factor_ID' : health_factor_ID })
    
    exist_check = cursor.fetchall()[0][0]
    
    if exist_check < 1:
    
        insert_stmt = ("INSERT INTO pubmed_has_health_factor (pubmed_pmid, health_factor_health_factor_ID,frequency) "
                     "VALUES (%s,%s,%s)")
    
        data = (pmid, health_factor_ID, frequency)
    
        cursor.execute(insert_stmt,data)
        cnx.commit()
    
    
# we gaan ervanuit dat de health_factor er al instaat want dat moet eerst gebeuren
def insert_pubmed_has_testsubject(pmid, testsubject, frequency, cnx):
    
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT testsubject_ID FROM testsubject WHERE naam = %(naam)s")
    cursor.execute(select_stmt, { 'naam': testsubject })
    
    result = cursor.fetchall()
    
    testsubject_ID = result[0][0]
    
    ## check if already existant
    select_stmt = ("SELECT count(1) "
                   "FROM pubmed_has_testsubject "
                   "WHERE pubmed_pmid = %(pmid)s "
                   "AND testsubject_testsubject_ID = %(testsubject_ID)s")
    cursor.execute(select_stmt, { 'pmid': pmid, 'testsubject_ID' : testsubject_ID })
    
    exist_check = cursor.fetchall()[0][0]
    
    if exist_check < 1:
    
        insert_stmt = ("INSERT INTO pubmed_has_testsubject (pubmed_pmid, testsubject_testsubject_ID) "
                     "VALUES (%s,%s)")
    
        data = (pmid, testsubject_ID)
    
        cursor.execute(insert_stmt,data)
        cnx.commit()
    
    
    
    
    

def main():
    
    cnx = get_conn()
    
    gewasNaam = "paardenbloem"
    compoundNaam = "grofvuil"
    health_factorNaam = "dodelijk"

    pmid = 13371337


    insert_pubmed(pmid,"baanbrekend", 1337,6,9,cnx) 
    insert_gewas(gewasNaam,cnx)
    insert_compound(compoundNaam,cnx)
    insert_health_factor(health_factorNaam,cnx)
    
    insert_pubmed_has_gewas(pmid, gewasNaam, 18,cnx)
    insert_pubmed_has_compound(pmid, compoundNaam, 22,cnx)
    insert_pubmed_has_health_factor(pmid,health_factorNaam,4,cnx)
    
    
    """
    print(insert_pubmed(101,"test titel",1337,6,9,cnx))
    
    print(insert_gewas("ketel",cnx))
    print(insert_health_factor("cancer",cnx))
    print(insert_compound("helium",cnx))
    print(insert_testsubject("octopus",cnx))
    """
    
main()