from flask import Flask, render_template, request
import json
import mysql.connector
import traceback

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

#Functie waar je ongein instouwt om een coole grafiek te kunnen genereren, potentieel AJAX
@app.route('/jsonstoreurl', methods = ['GET'])
def jsonstoreurl():
    
    cnx = mysql.connector.connect(user='owe8_pg1', 
                                  password='blaat1234',
                                  host='127.0.0.1',
                                  db="owe8_pg1")
    
    dic = {}
    thickest = 1
    
    dic["nodes"] = []
    dic["links"] = []
    
    cursor = cnx.cursor()
        
        #overly intesive, moet geoptimaliseerd worden.
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
        dickie = {"source" : a[3] , "target" : a[4], "value" : int(a[0])}
        thickest = min(thickest,a[0])  
        
        node = {"id" : a[3], "group" : a[1]}
        if node not in dic["nodes"]:
            dic["nodes"].append(node)
        
        node = {"id" : a[4], "group" : a[2]}
        if node not in dic["nodes"]:
            dic["nodes"].append(node) 
        
        dic["links"].append(dickie)
    
    
    
    dic["thickest"] = thickest
    cursor.close()
    cnx.close()
    
    with open('/home/owe8_pg1/public_html/static/javascript/data.json', 'w') as outfile:
        json.dump(dic, outfile)
        
    return "fixed it"
    

#maak die cache dood!!!!
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


# group1 = Compound
# group2 = Crop
# group3 = Health_benefit	
@app.route('/getPMIDinfo', methods=['GET'])
def getPMIDinfo():
    
    req_dic = request.args.to_dict()
    
    values = []
    
    for key in req_dic.keys():    
        waarde = req_dic[key]
        values.append(waarde)
      
    """
    query_piece1 =  """
                    #SELECT articles_terms.articles_id
                    #FROM articles_terms
                    #INNER JOIN terms ON articles_terms.terms_id = terms.id
                    #WHERE terms.mesh_term =  %s
    """
                    
    query_paster = "AND articles_terms.articles_id IN ("
    
    
    sel_query = query_piece1
    
    for term in values[1:]:
        
        sel_query += query_paster + query_piece1
    
    sel_query += len(values[1:])*")" + " LIMIT 25"
        
    cnx = mysql.connector.connect(user='owe8_pg1', 
                                  password='blaat1234',
                                  host='127.0.0.1',
                                  db='owe8_pg1')   
   
    cursor = cnx.cursor()
    
    cursor.execute(sel_query,values)
    rows = cursor.fetchall()
       
    id_list = [item for sublist in rows for item in sublist]
    
    id_string_list = []
    for ID in id_list:
        id_string_list.append(str(ID))
        
    
    query = ""
    if len(id_string_list) == 1:
        query = id_string_list[0]
    elif len(id_string_list) > 1:
        query = ','.join(id_string_list)
    else:
        return "Oh dear, no articles found"
    
    Entrez.email = 'huub.goltstein@gmail.com'
    handle = Entrez.esummary(db="pubmed", id=query, retmode="xml",retmax=25)
    records = Entrez.parse(handle)

    rijen = []
    
    for i,record in enumerate(records):
        tupletje = id_string_list[i], record['Title'].encode('utf-8')
        rijen.append(tupletje)
    
    
    
    color = ['red', 'orange', 'blue']
    count = 0
    terug = "<select style='margin: auto;'>"
    
    for pmid, titel in rijen:
        terug += "<option style='background-color: {};' value='opel'><a href='https://www.ncbi.nlm.nih.gov/pubmed/{}'>{}</a></option>".format(color[count], pmid, titel)
        count+=1
    
    terug += "</select>"
       
    """
    pubmedURL = "<a href='https://www.ncbi.nlm.nih.gov/pubmed/?term=" + "+".join(values) + "' target='_blank'>" + " and ".join(values) + "</a>"
    
    
    
    linked = " with ".join(values)
    return linked + "<br /><br />"+pubmedURL