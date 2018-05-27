from nltk import sent_tokenize, word_tokenize, pos_tag 
from pubmedRetrieval import search, fetch_details, get_PMID, get_title, get_abstract, get_article_date, get_keywords
import Database
import itertools

from collections import Counter
#import pubchempy as pch

#-----------------------------------------Het inlezen van de Pubmed data---------------------------------------------------------------
#Het aanmaken van een Publishment class die als attributen de data van NCBI Pubmed bevat die gebruikt gaat worden

class Publishment:
    def __init__(self, pubmedID, title, abstract, article_date, keywords):
        self.pubmedID = pubmedID
        self.title = title
        self.abstract = abstract
        self.article_date = article_date
        self.keywords = keywords     
        
    def __str__(self):
        return "(id: " + self.pubmedID + ",title: "+self.title +",date: "+self.article_date+",keywords: "+self.keywords +")"
        


def fill_data(search_word):
    results = search(search_word) #Zoeken naar een bepaald woord in Pubmed
    
    id_list = results['IdList'] #Een lijst maken van de results id's
    print('ok')
    papers = fetch_details(id_list) #haal hiervan de articles op.
    
    paper_object_list = make_paper_list(papers)
    print("oh")
    mainprocess(paper_object_list)
    

def make_paper_list(papers):
    paper_object_list = [] #Lijst voor de objecten 
    
    for i, paper in enumerate(papers['PubmedArticle']): #Een loop over alle artikelen
        
        try:
            paper = Publishment(get_PMID(paper),get_title(paper),get_abstract(paper),get_article_date(paper),get_keywords(paper))
            paper_object_list.append(paper) #Het object toevoegen aan de lijst met objecten
            
        except KeyError: #Artikel is incompleet
            pass
        
    return paper_object_list
    

#-----------------------------------------Het aanroepen en uitvoeren van alle functies--------------------------------------------------- 
    
def mainprocess(paper_object_list):
    
    cnx = Database.get_conn()
    
    
    
    organisms = ['momordica','charantia', 'melon', 'gourd','yam','potato','tomato']
    compounds = ['oxygen', 'hydrogen','glucose','vitamin','mineral','salt','sugar','toxin']
    benefits =  ['diabetes','obese','obesity','fattening']
    
    organisms = Database.get_crops(cnx)
    compounds = Database.get_compounds(cnx)
    benefits = Database.get_health_benefits(cnx)
    
    organisms_to_add = []
    compounds_to_add = []
    benefits_to_add = []
    articles_to_add = []
    
    
    for i,paper in enumerate(paper_object_list):
        
        PMID = paper.pubmedID
        Keywords = paper.keywords
        Titel = paper.title
        Abstract_tekst = paper.abstract
        publication_year = paper.article_date
        #print(paper.article_date)
        
        #insert_pubmed(PMID,titel,keywords,abstract,year,month,day, cnx):
        article = (PMID, Titel, Keywords, Abstract_tekst, publication_year)
        articles_to_add.append(article)
            
        abstract = str(paper.abstract).lower()
        sentences = preprocess(abstract)
        
        nouns = extract_nouns(sentences)
        
        teller = get_frequencies(nouns)
        
        for ding,znw in teller:
            
            
            
            if ding in organisms:
                organism = (PMID, ding , teller[(ding,znw)])
                organisms_to_add.append(organism)
                
            if ding in compounds:
                compound = (PMID, ding , teller[(ding,znw)])
                compounds_to_add.append(compound)
            
            if ding in benefits:
                benefit = (PMID, ding , teller[(ding,znw)])
                benefits_to_add.append(benefit)      
        
        
    #def insert_pubmed(PMID,titel,keywords,abstract,year,month,day, cnx):
    for article in articles_to_add:
        year = article[4]['Year']
        month = article[4]['Month']
        day = article[4]['Day']
        
        Database.insert_pubmed(article[0],article[1],article[2],article[3], int(year), int(month), int(day),cnx)
        
        
    for organism in organisms_to_add:
        Database.insert_Abstracten_has_crop(organism[0],organism[1],organism[2],cnx)
        
    for compounds in compounds_to_add:
        Database.insert_Abstracten_has_compound(compounds[0],compounds[1],compounds[2],cnx)
        
    for benefits in benefits_to_add:
        Database.insert_Abstracten_has_health_benefit(benefits[0],benefits[1],benefits[2],cnx)
    
    #print(organisms_to_add)
    #print(compounds_to_add)
    #print(benefits_to_add)
                    
 
#-----------------------------------------Preprocessing en Tokenizing--------------------------------------------------------------------    
#sent_tokenize, word_tokenize, pos_tag 
def preprocess(document):
    sentences = sent_tokenize(document)
    sentences = [word_tokenize(sent) for sent in sentences]
    sentences = [pos_tag(sent) for sent in sentences]
    return sentences

#-----------------------------------------Preprocessing, vinden zelfstandige naamwoorden en frequenties----------------------------------

def extract_nouns(sentences):
    sentences = list(itertools.chain(*sentences))
    
    #print("reeee:\n\n"+str(sentences)+"\n\n")
    nouns =  ([(word,tag) for word, tag in sentences if tag.startswith('NN')])
    #print(str(nouns) + "\n\n")
    return nouns
    

def get_frequencies(nouns):
    
    return Counter(nouns)

if __name__ == "__main__":
    fill_data("momordica charantia")