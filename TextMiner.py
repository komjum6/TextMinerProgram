from flask import Flask, render_template, request
import json
import mysql.connector
import traceback
import database
from pubmedRetrieval import search_domain

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

    tbo = error.__traceback__
    tb = traceback.extract_tb(tbo)
    
    return str(error) +">>" + str(tb)

#error 404 handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
	
#Functie waar je ongein instouwt om een coole grafiek te kunnen genereren, potentieel AJAX

#Functie waar je ongein instouwt om een coole grafiek te kunnen genereren,
#Momenteel slaat deze het op in een data.json bestand omdat het uitvoeren van deze taak 
#Zeer CPU intensief is en daarom het liefst zo min mogelijk gerunt dient te worden
@app.route('/jsonstoreurl', methods = ['GET'])
def jsonstoreurl():
    
    cnx = mysql.connector.connect(user='owe8_pg1', 
                                  password='blaat1234',
                                  host='127.0.0.1',
                                  db="owe8_pg1")
    
    dic = {}
    thickest = 1 #voor het bepalen van lijn diktes
    
    dic["nodes"] = []
    dic["links"] = []
    
    cursor = cnx.cursor()
        
        #overly intesive, moet geoptimaliseerd worden.
        #Omdat we elk artikel opvragen dat er mee te maken hebben en niet duidelijk genoeg gedefineert hebben dat het per se
        #iets te maken moet hebben met yams of bitter gourds, is de tussentabel gigantisch waardoor hij zeer sloom is
        #alle 6 de inner joins zijn nodig, maar de self join is gewoon zeer pittig om uit te voeren door het formaat van deze tabel
        #Om dit sneller te krijgen zou het beste eerst een query uitgevoert kunnen worden die alle artikelen ophaalt die iets te maken hebben
        #met de planten van interesse: Bitter gourd en Yam, maar de afgelopen dagen was cytosine te instabiel om goed te testen.
    sel_query = """
                SELECT COUNT( * ) , tt1.id, tt2.id, t1.mesh_term, t2.mesh_term
                FROM term_type AS tt1
                INNER JOIN terms AS t1 ON tt1.id = t1.term_type_id
                INNER JOIN articles_terms AS at1 ON at1.terms_id = t1.id
                INNER JOIN articles_terms AS at2 ON at1.articles_id = at2.articles_id
                AND at1.terms_id < at2.terms_id
                INNER JOIN terms AS t2 ON at2.terms_id = t2.id
                INNER JOIN term_type AS tt2 ON t2.term_type_id = tt2.id
                GROUP BY at1.terms_id, at2.terms_id
                """
                
    cursor.execute(sel_query) 
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"source" : a[3] , "target" : a[4], "value" : int(a[0])} #aanmaken van alle lijnen
        thickest = min(thickest,a[0])  
        
        node = {"id" : a[3], "group" : a[1]} #nodes van links
        if node not in dic["nodes"]:
            dic["nodes"].append(node)
        
        node = {"id" : a[4], "group" : a[2]} #nodes van rechts
        if node not in dic["nodes"]:
            dic["nodes"].append(node) 
        
        dic["links"].append(dickie)
    
    
    
    dic["thickest"] = thickest
    cursor.close()
    cnx.close()
    
    with open('/home/owe8_pg1/public_html/static/javascript/data.json', 'w') as outfile: #schrijf naar die file
        json.dump(dic, outfile)
        
    return "did it" #succes message
    

#Toegevoegd om te proberen hiermee de cache te omzeilen en alles te slopen,
#geen idee of het iets van nut heeft aangezien we niet bij de logs kunnen
#nog debug informatie kunnen opvragen of bij de settings van de apache webserver kunnen
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



@app.route('/getPMIDinfo', methods=['GET'])
def getPMIDinfo():
    
    try:
        req_dic = request.args.to_dict()
        
        
        
        values = []
        waarde = ""
        
        for key in req_dic.keys():    
            waarde = req_dic[key]
            values.append(waarde)
        
        if len(values) > 1:
        
            cnx = database.get_conn()    
            pmid_title_list = database.get_overlap_pmid_title(values[0],values[1],cnx)
            
            question = " AND ".join((values[0],values[1],))
            basic = search_domain() + " AND " + question
            
            cnx.close()        
            terug = "<a href='https://www.ncbi.nlm.nih.gov/pubmed/?term={}' target='_blank'>{}</a>".format(basic,question)
            terug = terug.replace("[","%5B").replace("]","%5D")
            terug += "<br />"
            terug += "<table>"
            terug += "<tr><th>Pubmed ID</th><th>Title</th></tr>"
            
            for pmid,title in pmid_title_list:
                terug += "<tr>"
                
                terug += "<td>{}</td><td><a href='https://www.ncbi.nlm.nih.gov/pubmed/{}' target='_blank'>{}</a></td>".format(str(pmid),str(pmid), title.encode('utf-8'))
                
                terug += "</tr>"
              
            terug += "</table>"
            return terug
            
        else:
            return "ERROR"
    except Exception as e:
        return str(e)