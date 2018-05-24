from flask import Flask, render_template
import json
import mysql.connector
app = Flask(__name__)



#De Root Map
@app.route('/')
def index():
    return render_template('index.html')
    
#De plaats waar alles gevisualiseerd word
@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html')

#De plaats voor contact info
@app.route('/contact')
def contact():
    return render_template('contact.html')

#Een plaats voor een introductie etc
@app.route('/about')
def about():
    return render_template('about.html')

#error 500 handling
@app.errorhandler(500)
def internal_error(error):

    return str(error)

#error 404 handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
	
#Functie waar je ongein instouwt om een coole grafiek te kunnen genereren, potentieel AJAX
@app.route('/jsonrequesturl')
def jsonrequesturl():
    
    cnx = mysql.connector.connect(user='owe8_pg1', password='blaat1234',
                              host='127.0.0.1',
                              db="owe8_pg1")
    
    dic = {}
    
    dic["nodes"] = []
    dic["links"] = []
    
    cursor = cnx.cursor()
    
    select_compounds = "SELECT Name FROM  Compound"
    cursor.execute(select_compounds)
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"id" : a, "group" : 1}
        
        dic["nodes"].append(dickie)
    
    
    select_crops = "SELECT Name FROM Crop" 
    cursor.execute(select_crops)  
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"id" : a, "group" : 2}
        
        dic["nodes"].append(dickie)
        
    
    select_health_benefit = "SELECT Name FROM Health_benefit" 
    cursor.execute(select_health_benefit)  
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"id" : a, "group" : 3}
        
        dic["nodes"].append(dickie)
    
    
    crop_compound = "SELECT Crop.Name, Compound.Name FROM Crop INNER JOIN Abstracten_has_Crop on Crop.Name = Abstracten_has_Crop.Crop_Name INNER JOIN Abstracten_has_Compound ON Abstracten_has_Crop.Abstracten_PMID = Abstracten_has_Compound.Abstracten_PMID INNER JOIN Compound on Compound.Name = Abstracten_has_Compound.Compound_Name"
    cursor.execute(crop_compound)  
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"source" : a[0], "target" : a[1], "value" : 1}
        
        dic["links"].append(dickie)
    
    
    compound_health_benefit = "SELECT Compound.Name, Health_benefit.Name FROM Compound INNER JOIN Abstracten_has_Compound on Compound.Name = Abstracten_has_Compound.Compound_Name INNER JOIN Abstracten_has_Health_benefit ON Abstracten_has_Compound.Abstracten_PMID = Abstracten_has_Health_benefit.Abstracten_PMID INNER JOIN Health_benefit on Health_benefit.Name = Abstracten_has_Health_benefit.Health_benefit_Name"
    cursor.execute(compound_health_benefit)  
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"source" : a[0], "target" : a[1], "value" : 8}
        
        dic["links"].append(dickie)
        
        
        
    crop_health_benefit = "SELECT Crop.Name, Health_benefit.Name FROM Crop INNER JOIN Abstracten_has_Crop on Crop.Name = Abstracten_has_Crop.Crop_Name INNER JOIN Abstracten_has_Health_benefit ON Abstracten_has_Crop.Abstracten_PMID = Abstracten_has_Health_benefit.Abstracten_PMID INNER JOIN Health_benefit on Health_benefit.Name = Abstracten_has_Health_benefit.Health_benefit_Name"
    cursor.execute(crop_health_benefit)  
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"source" : a[0], "target" : a[1], "value" : 16}
        
        dic["links"].append(dickie)
    
    cursor.close()
    cnx.close()
    
    return json.dumps(dic)

@app.route('/getPMIDinfo')
def getPMIDinfo():
    
    cnx = mysql.connector.connect(user='owe8_pg1', password='blaat1234',
                              host='127.0.0.1',
                              db="owe8_pg1")
    
    cnx.close()
    
    return "testerino"
    
    
    