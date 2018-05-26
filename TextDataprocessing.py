import nltk
from pubmedRetrieval import *
import itertools
from nltk.probability import FreqDist
import pubchempy as pch

#-----------------------------------------Het inlezen van de Pubmed data---------------------------------------------------------------
#Het aanmaken van een Publishment class die als attributen de data van NCBI Pubmed bevat die gebruikt gaat worden
def init_class(): #Deze wordt als eerste aangeroepen
    class Publishment:
        def __init__(self, pubmedID, title, abstract, article_date, keywords):
            self.pubmedID = pubmedID
            self.title = title
            self.abstract = abstract
            self.article_date = article_date
            self.keywords = keywords        
    fill_data(Publishment) #Aanroepen volgende functie met de class
    
def fill_data(Publishment):
    results = search('Momordica charantia') #Zoeken naar een bepaald woord in Pubmed
    id_list = results['IdList'] #Een lijst maken van de results
    papers = fetch_details(id_list) #Maak hier een variabele van
    
    paper_object_list = [] #Lijst voor de objecten 
       
    for i, paper in enumerate(papers['PubmedArticle']): #Een loop voor publicaties die terugkomen
        try:
            paper = Publishment(get_PMID(paper),get_title(paper),get_abstract(paper),get_article_date(paper),get_keywords(paper)) #Vullen van de class
            paper_object_list.append(paper) #Het object toevoegen aan de lijst met objecten
            
        except KeyError:
            pass
        
    Mainprocess(paper, paper_object_list) #Aanroepen volgende functie met de variabelen    

#-----------------------------------------Het aanroepen en uitvoeren van alle functies--------------------------------------------------- 
    
def Mainprocess(paper, paper_object_list):    
    sentences = [preprocess(str(paper.abstract)) for paper in paper_object_list] #Het preprocessen van de abstracten van de paper objecten
    nouns_abstract_list = extract_nouns(sentences) #Het extraheren van zelfstandige naamwoorden uit de abstracten
    list_of_all_dicts = get_frequencies(nouns_abstract_list) #Het maken van frequentie dictionaries uit de abstracten, index 0 hiervan is van de hele zoekopdracht en index 1 per abstract
    Frequency_dict_all = list_of_all_dicts[0] #Dit is dus de frequentie dictionary van alle abstracten van een zoekopdracht
    listy = list_of_all_dicts[1]
    
    organism_list = ['momordica', 'charantia', 'melon', 'gourd']
    compounds = ['oxygen', 'hydrogen']
    benefits = ['diabetes']
    
    for count, dicty in enumerate(listy):
        for word, frequency in dicty:
            if word in (organism_list + compounds + benefits):
                if word in organism_list:
                    print(str(count) + " " + word + " " + str(paper_object_list[count].pubmedID + " organism"))
                if word in compounds:
                    print(str(count) + " " + word + " " + str(paper_object_list[count].pubmedID + " compound"))
                if word in benefits:
                    print(str(count) + " " + word + " " + str(paper_object_list[count].pubmedID + " benefit"))
    #geen find_compounds

#-----------------------------------------Preprocessing en Tokenizing--------------------------------------------------------------------    
    
def preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def grammarize(sentence):
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(sentence)
    return result

#-----------------------------------------Preprocessing, vinden zelfstandige naamwoorden en frequenties----------------------------------

def extract_nouns(sentences, nouns_abstract_list = []):
    abstract_list = list(itertools.chain(*sentences))
    is_noun = lambda pos: pos[:2] == 'NN'
    for abstract in abstract_list:
        nouns = [word for (word, pos) in abstract if is_noun(pos)] #zelfstandige naamwoorden per abstract 
        nouns_abstract_list.append(nouns)
    return nouns_abstract_list

def get_frequencies(nouns_abstract_list, list_of_dicts = [], Frequency_dict_all = FreqDist()):
    for nouns in nouns_abstract_list:
        new_abstract = ''.join([(i + ' ') for i in nouns])
        words = nltk.tokenize.word_tokenize(new_abstract)
        list_of_dicts.append(Frequency_dict_all.most_common(len(nouns)))
        Frequency_dict_all.update(words)
    return [Frequency_dict_all,list_of_dicts]

#-----------------------------------------De data die de database via Database.py moet opslaan (zoals compounds)-------------------------

def find_compounds(Frequency_dict_all):
    listcompoundobject = []
    chemicals =[]

    for noun in Frequency_dict_all:
        if noun not in ['melon', 'AND', 'result', 'component', 'for', 'may' , 'male', 'equal', 'control', 'access', 'we', 'side', 'target', 'action'] : #Sorry dat het hardcoded moet, maar ik wil geen chemische verbinding genaamd melon
            results = pch.get_compounds(noun, 'name')
            if results != []:
                chemicals.append(noun)
                listcompoundobject.append(results[0])
                
    #for noun in Frequency_dict_all:
    #    results = pch.get_compounds(noun, 'name')
    #    if results != []:
    #        chemicals.append(noun)
    #        listcompoundobject.append(results[0])
    return chemicals
    #print(listcompoundobject)
    #print('-'*10 + '\n')

    #for compound in listcompoundobject:
    #    print(compound.molecular_formula)
    #    print('-'*5 + '\n' + compound.iupac_name + '\n')

    #print('\n' + str(chemicals))