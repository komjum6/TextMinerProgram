from nltk import sent_tokenize, word_tokenize, pos_tag

from pubmedRetrieval import search, fetch_details, get_PMID, get_title,get_abstract,get_article_date,get_keywords
import itertools
from nltk.probability import FreqDist

#-----------------------------------------Het inlezen van de Pubmed data---------------------------------------------------------------
#Het aanmaken van een Publishment class die als attributen de data van NCBI Pubmed bevat die gebruikt gaat worden

class Publishment:
    def __init__(self, pubmedID, title, abstract, article_date, keywords):
        self.pubmedID = pubmedID
        self.title = title
        self.abstract = abstract
        self.article_date = article_date
        self.keywords = keywords        
    
def fill_data(searchword):
    results = search(searchword) #Zoeken naar een bepaald woord in Pubmed
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
    
    print(paper_object_list[2].abstract)
    
    organisms = ['momordica charantia', 'melon', 'gourd']
    compounds = ['oxygen', 'hydrogen']
    benefits = ['diabetes']
    
    organisms2 = underscorify(organisms)
    compounds2 = underscorify(compounds)
    benefits2 = underscorify(benefits)
    
    
    sentences = []
    for paper in paper_object_list:
        blad = str(paper.abstract).lower()
        blad = underscorify_abstract(organisms,organisms2,blad)
        blad = underscorify_abstract(compounds,compounds2,blad)
        blad = underscorify_abstract(benefits,benefits2,blad)
        sentences.append(preprocess(blad))
    
    nouns_abstract_list = extract_nouns(sentences) #Het extraheren van zelfstandige naamwoorden uit de abstracten
    list_of_all_dicts = get_frequencies(nouns_abstract_list) #Het maken van frequentie dictionaries uit de abstracten, index 0 hiervan is van de hele zoekopdracht en index 1 per abstract
    listy = list_of_all_dicts[1]
    
   
    print("hoi: "+str(listy))
    
    for count, dicty in enumerate(listy):
        for word, frequency in dicty:
            if word in (organisms2 + compounds2 + benefits2) and count < 4:
                if word in organisms:
                    print(str(count) + " " + word + " " + str(paper_object_list[count].pubmedID + " organism") + str(frequency))
                if word in compounds:
                    print(str(count) + " " + word + " " + str(paper_object_list[count].pubmedID + " compound") + str(frequency))
                if word in benefits:
                    print(str(count) + " " + word + " " + str(paper_object_list[count].pubmedID + " benefit") + str(frequency))
    #geen find_compounds

def underscorify_abstract(original, replaced, abstract):
    
    for i, word in enumerate(replaced):
        if word is not original[i]:
            abstract = abstract.replace(original[i],word)
        
    return abstract


def underscorify(lijst):
    nieuwe_lijst = []
    for word in lijst:
        nieuwe_lijst.append(word.replace(" ",""))
    return nieuwe_lijst

#-----------------------------------------Preprocessing en Tokenizing--------------------------------------------------------------------    
    
def preprocess(document):
    sentences = sent_tokenize(document)
    sentences = [word_tokenize(sent) for sent in sentences]
    sentences = [pos_tag(sent) for sent in sentences]
    return sentences

#-----------------------------------------Preprocessing, vinden zelfstandige naamwoorden en frequenties----------------------------------

def extract_nouns(sentences, nouns_abstract_list = []):
    abstract_list = list(itertools.chain(*sentences))
    
    print(abstract_list)
    
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
