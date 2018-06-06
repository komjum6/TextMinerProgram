from flask import Flask, render_template, request
import json
import mysql.connector
import database
from pubmedRetrieval import search_domain

app = Flask(__name__)

#De Root Map, simpele index.html
@app.route('/')
def index():
    return render_template('index.html')
    
#De plaats waar alles gevisualiseerd word
#Een groot deel van de daatwerkelijke functionaliteit zit in de javascript
#Flask is er eigenlijk alleen voor portability en om te callen met javascript
@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html')

#De plaats voor contact info, een simpele contact.html
@app.route('/contact')
def contact():
    return render_template('contact.html')

#Een plaats voor een introductie etc, simpele about.html
@app.route('/about')
def about():
    return render_template('about.html')

#error 500 handling 
#Dit zou nooit moeten voorkomen, en retourneert de error als String, met een vriendelijk berichtje.
@app.errorhandler(500)
def internal_error(error):
    
    return "Please report this error message: " + str(error)

#error 404 handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
	
#Functie waar je ongein instouwt om een coole grafiek te kunnen genereren,
#Momenteel slaat deze het op in een data.json bestand omdat het uitvoeren van deze taak 
#Potentieel zeer CPU intensief mits de database groot genoeg is door een gigantische selfjoin
#Of de SQL server belasten of Python belasten was de keuze.
#Niet bedoeld voor aanroepen gebruiker.
@app.route('/jsonstoreurl', methods = ['GET'])
def jsonstoreurl():
    
    cnx = mysql.connector.connect(user='owe8_pg1', 
                                  password='blaat1234',
                                  host='127.0.0.1',
                                  db="owe8_pg1")
    
    dic = {}
    thickest = 1 #voor het bepalen van lijn diktes
    
    dic["nodes"] = [] #de nodes
    dic["links"] = [] #de links
    
    cursor = cnx.cursor()
        
        #Omdat het domein beperkt is tot de ongeveer ~2200 as of juni 2018 artikelen
        #Is deze query zeer snel en er is geprobeert door het aanleggen van verschillende
        #indexes om de Query sneller te laten verlopen door de opties die de 
        #Query analyser heeft te vergroten.
        #In essentie precies hetzelfde als de functie voor het ophalen van de informatie uit de links
        #Tussen twee artikelen, de data wordt zo compact opgeslagen,
        #Zodat de server niet hapert als er veel data verzonden wordt
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
        dickie = {"source" : a[3] , "target" : a[4], "value" : int(a[0])} #aanmaken van alle lijnen, term -> term, met als value de count(*)
        thickest = min(thickest,a[0])  
        
        node = {"id" : a[3], "group" : a[1]} #nodes van links
        if node not in dic["nodes"]:
            dic["nodes"].append(node)
        
        node = {"id" : a[4], "group" : a[2]} #nodes van rechts
        if node not in dic["nodes"]:
            dic["nodes"].append(node) 
        
        dic["links"].append(dickie) #daadwerkelijk toevoegen van de link
    
    
    
    dic["thickest"] = thickest #zodat de lijntjes relatief aan de aller dikste gemaakt kunnen worden
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


#Functie voor het generen van een Tabel met pmid, titel van artikels en
#Voor het hackishly genereren van een link naar pubmed met hierin een query 
#Die ongeveer equivalent is aan de queries voor het verzamelen van de data
#Dit om de betrouwbaarheid aan te kunnen tonen
#Zodat de gebruiker niet de drang krijgt handmatig te controleren of
#de gevonden resultaten betrouwbaar zijn.
@app.route('/getPMIDinfo', methods=['GET'])
def getPMIDinfo():
    
    try:
        req_dic = request.args.to_dict() #verschillende argumenten, de naam van de variabelen is arbitrair
        
        values = []
        waarde = ""
        
        for key in req_dic.keys(): #pak alle termen.
            waarde = req_dic[key]
            values.append(waarde)
        
        if len(values) > 1: #er moeten wel 2 termen zijn om een overlap te hebben
        
            cnx = database.get_conn()    
            pmid_title_list = database.get_overlap_pmid_title(values[0],values[1],cnx) #we gebruiken alleen de eerste 2 termen omdat dit simpeler is
            cnx.close() #ZSM connectie sluiten zodat als het script gestopt wordt, die niet blijft hangen
            
            question = " AND ".join((values[0],values[1],))
            basic = search_domain() + " AND " + question
              
            
            terug = "<a href='https://www.ncbi.nlm.nih.gov/pubmed/?term={}' target='_blank'>{}</a>".format(basic,question) #leuke link naar pubmed, want <3 pubmed
            terug = terug.replace("[","%5B").replace("]","%5D") #haakjes enzo door HTML troep vervangen
            
            table = "<table><tr><th>Pubmed link</th><th>Saveable link to table</th></tr>" #table headers
            link = "<a href='{}' target='_blank'>Saveable overlap</a>".format(str(request.url)) #de link naar alleen de return zodat dit later opgevraagt kan worden of zelfs gebookmarkt kan worden
            table += "<tr><td>{}</td><td>{}</td></tr>".format(terug,link) #de row met de inhoudt voor de table
            terug = table + "</table>"
            
            terug += "<br /><br />"
            terug += "<table>"
            terug += "<tr><th>Pubmed ID</th><th>Title</th></tr>"
            
            for pmid,title in pmid_title_list: #loopen over de pmids/titles en TR's van maken
                terug += "<tr>"
                
                terug += "<td>{}</td><td><a href='https://www.ncbi.nlm.nih.gov/pubmed/{}' target='_blank'>{}</a></td>".format(str(pmid),str(pmid), title.encode('utf-8')) #UTF-8 want unicode, pubmed linkjes bevatten gewoon het pubmedID, super chill.
                
                terug += "</tr>"
              
            terug += "</table>"
            return terug
            
        else:
            return "ERROR" #Debug code.
    except Exception as e:
        return str(e)