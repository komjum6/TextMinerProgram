#Voorbeeld van een artikel over de Bitter Gourd

document = \
"""Abstract
Background
Bitter melon (Momordica charantia) is a commonly used food crop for management of a variety of diseases most notably for control of diabetes, a disease associated with aberrant inflammation.

Purpose
To evaluate the anti-inflammatory property of BG-4, a novel bioactive peptide isolated from the seed of bitter melon.

Methods
Differentiated THP-1 human macrophages were pre-treated with BG-4 and stimulated with lipopolysaccharide. Pro-inflammatory cytokines IL-6 and TNF-α were measured by enzyme-linked immunosorbent assay. The mechanism of action involving activation of NF-κB and phosphorylation of ERK and STAT3 was measured by western blot and immunofluorescence. The production of intracellular reactive oxygen species was evaluated by fluorescence microscopy and fluorescence spectrophotometry.

Results
BG-4 dose dependently reduce the production of pro-inflammatory cytokines IL-6 and TNF-α. The ability of BG-4 to reduce production of cytokines are associated with reduced phosphorylation of ERK and STAT3 accompanied by reduced nuclear translocation of p65 NF-κB subunit. The mechanism of action is reduction of LPS-induced production of intracellular reactive oxygen species.

Conclusion
Our results demonstrated the ability of BG-4, a novel peptide from the seed of bitter melon, to exert anti-inflammatory action. This could explain the traditional use of bitter melon against diseases associated with aberrant and uncontrolled inflammation."""

import nltk
from pubmedRetrieval import *
import itertools
from nltk.probability import FreqDist
import pubchempy as pch

def init_class():
    class Publishment:
        def __init__(self, pubmedID, title, abstract, article_date, keywords):
            self.pubmedID = pubmedID
            self.title = title
            self.abstract = abstract
            self.article_date = article_date
            self.keywords = keywords        
    fill_data(Publishment)
    
def fill_data(Publishment):
    results = search('Momordica charantia')
    id_list = results['IdList'] #kan dit weg?
    papers = fetch_details(id_list)
    
    paper_object_list = []
       
    for i, paper in enumerate(papers['PubmedArticle']):
        try:
            paper = Publishment(get_PMID(paper),get_title(paper),get_abstract(paper),get_article_date(paper),get_keywords(paper))
            paper_object_list.append(paper)
            
        except KeyError:
            pass
    
    sentences = [preprocess(str(paper.abstract)) for paper in paper_object_list]
    nouns = extract_nouns(sentences)
    list_of_all_dicts = get_frequencies(nouns)
    Frequency_dict_all = list_of_all_dicts[0]
    for word, frequency in Frequency_dict_all.most_common(len(nouns)):
        print(u'{};{}'.format(word, frequency))
    find_compounds(Frequency_dict_all)

def preprocess(document = document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def grammarize(sentence):
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(sentence)
    return result

def extract_nouns(sentences):
    abstract = list(itertools.chain(*sentences))
    is_noun = lambda pos: pos[:2] == 'NN' 
    nouns = [word for (word, pos) in abstract if is_noun(pos)] 
    return nouns

def get_frequencies(nouns, list_of_dicts = [], Frequency_dict_all = FreqDist()):
    new_abstract = ''.join([(i + ' ') for i in nouns])
    words = nltk.tokenize.word_tokenize(new_abstract)
    list_of_dicts.append(Frequency_dict_all.most_common(len(nouns)))
    Frequency_dict_all.update(words)
    return [Frequency_dict_all,list_of_dicts]

def find_compounds(Frequency_dict_all):
    listcompoundobject = []
    chemicals =[]

    for noun in Frequency_dict_all:
        if noun not in ['melon', 'AND', 'result', 'component', 'for', 'may' , 'male', 'equal', 'control', 'access', 'we', 'side', 'target', 'action'] : #Sorry dat het hardcoded moet, maar ik wil geen chemische verbinding genaamd melon
            results = pch.get_compounds(noun, 'name')
            if results != []:
                chemicals.append(noun)
                listcompoundobject.append(results[0])

    print(listcompoundobject)
    print('-'*10 + '\n')

    for compound in listcompoundobject:
        print(compound.molecular_formula)
        print('-'*5 + '\n' + compound.iupac_name + '\n')

    print('\n' + str(chemicals))