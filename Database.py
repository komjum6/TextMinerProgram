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
    
    cnx = mysql.connector.connect(user='owe8_pg1', password='blaat1234',
                              host='127.0.0.1',
                              db='owe8_pg1')
    return cnx

def commit_conn(cnx):
    cnx.commit()
    cnx.close()

def insert_pubmed(PMID,titel,keywords,abstract,year,month,day, cnx):
    
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT PMID FROM Abstracten WHERE PMID = %(PMID)s")
    cursor.execute(select_stmt, {'PMID' : PMID})
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        cursor.close()
        return result[0][0]
    else:

        insert_statement = ("INSERT INTO Abstracten (PMID, keywords, titel, Abstract_tekst, Publication_year) "
                     "VALUES (%s,%s,%s,%s,%s)")
        data = (PMID,keywords, titel,abstract, datetime.date(year, month, day))
    
        cursor.execute(insert_statement,data)
        
        
        select_stmt = ("SELECT PMID FROM Abstracten WHERE PMID = %(PMID)s")
        cursor.execute(select_stmt, {'PMID' : PMID})
        result = cursor.fetchall()
        cursor.close()
        return result[0][0]
        

def get_health_benefits(cnx):

    cursor = cnx.cursor()
    select_stmt = "SELECT Name FROM Health_benefit"
    cursor.execute(select_stmt)
    
    health_benefit_list = []
    for naam in cursor:
        health_benefit_list.append(naam[0])
    cursor.close()
    return health_benefit_list

def get_crops(cnx):

    cursor = cnx.cursor()
    select_stmt = "SELECT Name FROM Crop"
    cursor.execute(select_stmt)
    
    crop_list = []
    for naam in cursor:
        crop_list.append(naam[0])
    cursor.close()
    return crop_list

def get_compounds(cnx):

    cursor = cnx.cursor()
    select_stmt = "SELECT Name FROM Compound"
    cursor.execute(select_stmt)
    
    compound_list = []
    for naam in cursor:
        compound_list.append(naam[0])
    cursor.close()
    return compound_list
        
    

def insert_crop(naam, cnx):
    
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT Name FROM Crop WHERE Name = %(naam)s")
    cursor.execute(select_stmt, { 'naam': naam })
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        cursor.close()
        return result[0][0]
        
    else:        
        insert_stmt = ("INSERT INTO Crop (Name) "
                     "VALUES (%s)")
        
        cursor.execute(insert_stmt,(naam,))
        cursor.close()
        
        
        
def insert_compound(naam, cnx):
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT Name FROM Compound WHERE Name = %(Naam)s")
    cursor.execute(select_stmt, { 'Naam': naam })
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        cursor.close()
        return result[0][0]
        
    else:        
        insert_stmt = ("INSERT INTO Compound (Name) "
                     "VALUES (%s)")
        
        cursor.execute(insert_stmt,(naam,))
        cursor.close()
    

def insert_health_benefit(naam, cnx):
    cursor = cnx.cursor()
    
    select_stmt = ("SELECT Name FROM Health_benefit WHERE Name = %(naam)s")
    cursor.execute(select_stmt, { 'naam': naam })
    
    result = cursor.fetchall()
    
    if len(result) > 0:
        cursor.close()
        return result[0][0]
        
    else:        
        insert_stmt = ("INSERT INTO Health_benefit (Name) "
                     "VALUES (%s)")
        cursor.close()
        cursor.execute(insert_stmt,(naam,))
        
    
# we gaan ervanuit dat de compound er al instaat, want dat moet eerst gebeuren
def insert_Abstracten_has_compound(pmid, compound, count, cnx):
    
    cursor = cnx.cursor()
    
    ## check if already existant
    select_stmt = ("SELECT count(1)"
                   "FROM Abstracten_has_Compound "
                   "WHERE Abstracten_PMID = %(pmid)s "
                   "AND Compound_Name = %(compound_ID)s")
    cursor.execute(select_stmt, { 'pmid': pmid, 'compound_ID' : compound })
    
    exist_check = cursor.fetchall()[0][0]
    
    if exist_check < 1:
    
    
        insert_stmt = ("INSERT Abstracten_has_Compound (Abstracten_PMID, Compound_Name, Count) "
                     "VALUES (%s,%s,%s)")
    
        data = (pmid, compound, count)
    
        cursor.execute(insert_stmt,data)
        cursor.close()
   
    
    
# we gaan ervanuit dat het gewas er al instaat, want dat moet eerst gebeuren
def insert_Abstracten_has_crop(pmid, crop, count, cnx):
    
    cursor = cnx.cursor()

    
    ## check if already existant
    select_stmt = ("select count(1) "
                   "FROM Abstracten_has_Crop "
                   "WHERE Abstracten_PMID = %(pmid)s "
                   "AND Crop_Name = %(crop)s")
    cursor.execute(select_stmt, { 'pmid': pmid, 'crop' : crop })
    
    exist_check = cursor.fetchall()[0][0]
    
    if exist_check < 1:
    
    
        insert_stmt = ("INSERT INTO Abstracten_has_Crop (Abstracten_PMID, Crop_Name, Count) "
                     "VALUES (%s,%s,%s)")
    
        data = (pmid, crop, count)
    
        cursor.execute(insert_stmt,data)
        cursor.close()
    else:
        cursor.close()
    
    
# we gaan ervanuit dat de health_factor er al instaat want dat moet eerst gebeuren
def insert_Abstracten_has_health_benefit(pmid, health_benefit, count, cnx):
    
    cursor = cnx.cursor()
    
    ## check if already existant
    select_stmt = ("SELECT count(1) "
                   "FROM Abstracten_has_Health_benefit "
                   "WHERE Abstracten_PMID = %(pmid)s "
                   "AND Health_benefit_Name = %(health_benefit)s")
    cursor.execute(select_stmt, { 'pmid': pmid, 'health_benefit' : health_benefit })
    
    exist_check = cursor.fetchall()[0][0]
    
    if exist_check < 1:
    
        insert_stmt = ("INSERT INTO Abstracten_has_Health_benefit (Abstracten_PMID, Health_benefit_Name, Count) "
                     "VALUES (%s,%s,%s)")
    
        data = (pmid, health_benefit, count)
    
        cursor.execute(insert_stmt,data)
        cursor.close()
    else:
        cursor.close()

def main():
    
    cnx = get_conn()
    
    gewasNaam = "paardenbloem"
    compoundNaam = "grofvuil"
    health_factorNaam = "dodelijk"

    pmid = 13371337

    insert_pubmed(pmid,"hoi","1,2,3","stom abstract",1337,6,9,cnx)
    
    insert_crop(gewasNaam,cnx)
    insert_compound(compoundNaam,cnx)
    insert_health_benefit(health_factorNaam,cnx)
    
    insert_Abstracten_has_health_benefit(pmid,health_factorNaam,69,cnx)
    
    insert_Abstracten_has_compound(pmid, compoundNaam, 23, cnx)
    
    insert_Abstracten_has_crop(pmid,gewasNaam,420,cnx)