import spacy
import csv
import re
import pandas as pd
nlp = spacy.load("en_core_web_lg")
from sentence_transformers import SentenceTransformer, util
import torch

embedder = SentenceTransformer('all-MiniLM-L6-v2')



def read_taxonomies(tax):
    list_tax=list()
    with open(tax, 'r') as file:
        csvreader = csv.reader(file)
        for i in csvreader:
            list_tax.append([i[0], i[8]])
    return list_tax

def read_taxonomies2(tax):
    list_tax=list()
    df1 = pd.read_csv('skos_uri.csv')
    list_tax.append([df1['Id'], df1['skos:prefLabel@en']])
    return list_tax


def read_documents(doc):
    text=list()
    
    with open(doc, 'r') as file:
        csvreader = csv.reader(file)
        for i in csvreader:
            #print(i[0],i[7])
            clean = re.sub(r'[^\w\s]+','',i[7])
            tokens_text=nlp(clean)
            tokens_list=list()
            for token in tokens_text:
                #print(token)
                tokens_list.append(token)
            #print(i[0], tokens_list)
            text.append([i[0],clean, tokens_list])
    #print(text)
    return(text)


def read_documents2(doc):
    text=list()
    issues=list()
    details=list()
    issue_text=list()
    df1 = pd.read_csv('corpus_aiact.csv')
    #print(df1['ISSUES'])
    clean = re.sub(r'[^\w\s]+','',str(df1['TEXT']))
    tokens_text=nlp(clean)
    tokens_list=list()
    for token in tokens_text:
        tokens_list.append(token)
    
    text.append([df1['NAME_DOC'],clean, tokens_list])
    issues.append([df1['NAME_DOC'], df1['ISSUES']])
    details.append([df1['NAME_DOC'], df1['ISSUES'], clean])
    
    row=0
    for row in range(len(df1)):
        if (isinstance(df1.iloc[row]['ISSUES'], str)):
            separate_issue=df1.iloc[row]['ISSUES'].split(';')
            for i in separate_issue:
                clean = re.sub(r'[^\w\s]+','',str(df1.iloc[row]['TEXT']))
                #print(row,'->',separate_issue,'--',i, '----', clean )
                issue_text.append([i.strip(), clean])
                
        row=row+1
    
    return(text, issues, issue_text)

def similar(list_issue_text):
    for doc in list_issue_text:
        issue=nlp(doc[0])
        text=nlp(doc[1])
        print(issue, text)
        print(issue.similarity(text))

def sentences_embedings(list_issue_text):
    #texf from documents
    corpus=list()
    issues=list()
    for i in list_issue_text:
        issues.append(i[0])
        corpus.append(i[1])
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    print(corpus)
    '''
    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    top_k = min(5, len(corpus))
    for query in issues:
        query_embedding = embedder.encode(query, convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 5 most similar sentences in corpus:")

        for score, idx in zip(top_results[0], top_results[1]):
            print(corpus[idx], "(Score: {:.4f})".format(score))


            '''



text=read_documents2('archivo/corpus_aiact.csv')
#print(text)
tax=read_taxonomies2('skos_uri.csv')
#similar(text[2])
sentences_embedings(text[2])   