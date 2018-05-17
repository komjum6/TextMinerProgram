#https://stackoverflow.com/questions/4951751/creating-a-new-corpus-with-nltk
#http://www.nltk.org/book/ch07.html
#https://blog.algorithmia.com/acquiring-data-for-document-classification/
#http://d.hatena.ne.jp/tdm/20080228/1204213888
#https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/

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
from pubmedRetrieval import search, fetch_details

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

def get_abstracts():
    results = search('Momordica charantia')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers):
        print(str(i) + ":" + paper)
        
    #for i, paper in enumerate(papers['PubmedArticle']):
        #print(str(i) + ":"+ str(paper['MedlineCitation']['KeywordList']))
        #print(str(i) + ":"+ str(paper['MedlineCitation']['Article']['ArticleDate']))
        #print(str(i) + ":"+ str(paper['MedlineCitation']['PMID']))
        #print(str(i) + ":"+ str(paper['MedlineCitation']['Article']['Abstract']['AbstractText']))
