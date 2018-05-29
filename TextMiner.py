from flask import Flask, render_template, request
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
@app.route('/jsonrequesturl', methods = ['GET'])
def jsonrequesturl():
    
    cnx = mysql.connector.connect(user='owe8_pg1', password='blaat1234',
                              host='127.0.0.1',
                              db="owe8_pg1")
    
    dic = {}
    thickest = 1
    toHide = request.args.get('toHide')
    
    
    dic["nodes"] = []
    dic["links"] = []
    
    cursor = cnx.cursor()
    
    #zodat nodes als ze geen verbinding hebben weg zijn
    select_compounds =  """ 
                        SELECT DISTINCT(compound.Compound_Name) 
                        FROM Abstracten_has_Compound as compound
                        """



    cursor.execute(select_compounds)
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"id" : a, "group" : 1}
        
        dic["nodes"].append(dickie)
    
    
    select_crops =  """
                    SELECT DISTINCT(crop.Crop_Name) 
                    FROM Abstracten_has_Crop as crop  
                    """ 
                    
    cursor.execute(select_crops)  
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"id" : a, "group" : 2}
        
        dic["nodes"].append(dickie)
        
    
    select_health_benefit = """
                            SELECT DISTINCT(health.Health_benefit_Name) 
                            FROM Abstracten_has_Health_benefit as health  
                            """ 
                            
    cursor.execute(select_health_benefit)  
    fetchall = cursor.fetchall()
    
    for a in fetchall:
        dickie = {"id" : a, "group" : 3}
        
        dic["nodes"].append(dickie)
    
    if(toHide != "cropcompound"): #cropcompound of compoundhealthbenefit of crophealthbenefit
        crop_compound = """
                        SELECT crop.Crop_Name, compound.Compound_Name, COUNT( * ) 
                        FROM Abstracten_has_Crop AS crop 
                        INNER JOIN Abstracten_has_Compound AS compound ON crop.Abstracten_PMID = compound.Abstracten_PMID 
                        GROUP BY crop.Crop_Name, compound.Compound_Name 
                        """
        
        
        
        cursor.execute(crop_compound)  
        fetchall = cursor.fetchall()
    
        for a in fetchall:
            dickie = {"source" : a[0], "target" : a[1], "value" : int(a[2])}
            thickest = min(thickest,a[2])
            dic["links"].append(dickie)
    
    if(toHide != "compoundhealthbenefit"):
        compound_health_benefit = """
                                SELECT compound.Compound_Name, health.Health_benefit_Name, COUNT( * ) 
                                FROM Abstracten_has_Compound AS compound 
                                INNER JOIN Abstracten_has_Health_benefit AS health ON compound.Abstracten_PMID = health.Abstracten_PMID 
                                GROUP BY compound.Compound_Name, health.Health_benefit_Name 
                                """
                        
        cursor.execute(compound_health_benefit)  
        fetchall = cursor.fetchall()
        
        for a in fetchall:
            dickie = {"source" : a[0], "target" : a[1], "value" : a[2]}
            thickest = min(thickest,a[2])
            dic["links"].append(dickie)
        
        
    if(toHide != "crophealthbenefit"):   
        crop_health_benefit = """
                            SELECT crop.Crop_Name, health.Health_benefit_Name, COUNT( * ) 
                            FROM Abstracten_has_Crop AS crop 
                            INNER JOIN Abstracten_has_Health_benefit AS health ON crop.Abstracten_PMID = health.Abstracten_PMID 
                            GROUP BY crop.Crop_Name, health.Health_benefit_Name 
                            """
        
        cursor.execute(crop_health_benefit)  
        fetchall = cursor.fetchall()
        
        for a in fetchall:
            dickie = {"source" : a[0], "target" : a[1], "value" : a[2]}
            thickest = min(thickest,a[2])
            dic["links"].append(dickie)
    dic["thickest"] = thickest
    cursor.close()
    cnx.close()
    
    return json.dumps(dic)

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
    
    req2_dic = {}
    
    for key in req_dic.keys():
        req2_dic[str(key)] = str(req_dic[key])
    
    req_dic = req2_dic
    
    query = ""
    
    if 'Compound' in req_dic and 'Crop' in req_dic:
        
        query = ("SELECT compound.Abstracten_PMID, Abstracten.Titel FROM Abstracten_has_Compound as compound INNER JOIN Abstracten_has_Crop as crop on compound.Abstracten_PMID = crop.Abstracten_PMID INNER JOIN Abstracten on Abstracten.PMID = compound.Abstracten_PMID "
                "WHERE compound.Compound_name = %(Compound)s AND crop.Crop_name = %(Crop)s")
        
    elif 'Compound' in req_dic and 'Health_benefit' in req_dic:
        
        query = ("SELECT compound.Abstracten_PMID, Abstracten.Titel FROM Abstracten_has_Compound as compound INNER JOIN Abstracten_has_Health_benefit as health on compound.Abstracten_PMID = health.Abstracten_PMID INNER JOIN Abstracten on Abstracten.PMID = compound.Abstracten_PMID "
                "WHERE compound.Compound_name = %(Compound)s AND health.Health_benefit_name = %(Health_benefit)s")
        
    elif 'Crop' in req_dic and 'Health_benefit' in req_dic:
        query = ("SELECT crop.Abstracten_PMID, Abstracten.Titel FROM Abstracten_has_Crop as crop INNER JOIN Abstracten_has_Health_benefit as health on crop.Abstracten_PMID = health.Abstracten_PMID INNER JOIN Abstracten on Abstracten.PMID = crop.Abstracten_PMID "
                "WHERE crop.Crop_name = %(Crop)s AND health.Health_benefit_name = %(Health_benefit)s")
        
    else:
        pass

    try:
        cnx = mysql.connector.connect(user='owe8_pg1', password='blaat1234',
                                      host='127.0.0.1',
                                      db="owe8_pg1")
        cursor = cnx.cursor()
        cursor.execute(query,params=req_dic)
        result = cursor.fetchall()
        #lit lijstje met id's.
        terug = ""
        for (pmid, titel) in result:
            terug += "<a href='"
            terug += "https://www.ncbi.nlm.nih.gov/pubmed/" + str(pmid)
            terug += "'>"
            terug += str(titel)
            terug += "</a><br /><br />"
        return terug
            
        
        
    except Exception as e:
        ret_string = str(e)
        ret_string += "<<<<>>>>"
        ret_string += query
        ret_string += "<<<<>>>>"
        ret_string += str(req_dic)
        return ret_string
    finally:
        cursor.close()
        cnx.close()
        
    return "wow wacht wat"