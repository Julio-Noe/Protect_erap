import spacy
import csv
import re
import pandas as pd
import random
import json
from spacy.training.example import Example
from spacy.util import minibatch, compounding
from pathlib import Path
#nlp = spacy.load("en_core_web_lg")
# Getting the pipeline component
#ner=nlp.get_pipe("ner")

def read_taxonomies2(tax):
    list_tax=list()
    df1 = pd.read_csv('skos_uri.csv')
    list_tax.append([df1['Id'], df1['skos:prefLabel@en']])
    return list_tax


def read_documents2(doc):
    text=list()
    df1 = pd.read_csv('corpus_aiact.csv')
    #print(df1['ISSUES'])
    clean = re.sub(r'[^\w\s]+','',str(df1['TEXT']))
    tokens_text=nlp(clean)
    tokens_list=list()
    for token in tokens_text:
        #print(token)
        tokens_list.append(token)
    #print(i[0], tokens_list)
    text.append([df1['NAME_DOC'],clean, tokens_list])
    #print(text)
    return(text)

def similar(list_doc, list_tax):
    for doc in list_doc:
        id_doc=doc[0]
        text=doc[1]
        print(id_doc, text)


def get_corpus_bert1(doc):
    text=list()
    with open(doc, 'r') as file: #csv donde vienen los datos
        csvreader = csv.reader(file)
        for i in csvreader:
            clean = re.sub(r'[^\w\s]+','',i[7])
            document = nlp(clean)
            #print("-------------Sentences: ", i[0])
            for j,s in enumerate(document.sents):
                #print(j,s)
                for token in s:
                    #print('\t',token.orth_, token.pos_)
                    text.append([s, token.orth_, token.pos_, i[6], clean])
   
    return (text)

def ner1(doc): #funcion para obtener tabla con [idnumerodoc_numerosentencia, sentencia]
    nlp = spacy.load("en_core_web_lg")
    table1=list()
    with open(doc, 'r') as file: #csv donde vienen los datos
        csvreader = csv.reader(file)
        for i in csvreader:
            clean = re.sub(r'[^\w\s]+','',i[7])
            document = nlp(clean)
            #print("-------------Sentences: ", i[0])
            for j,s in enumerate(document.sents):
                ide='id'+str(i[0])+str(j)
                #print(ide, s)
                table1.append([ide, s])
    return table1
    
                    
def read_my_vocabulary(tax): #funcion para leer la propia taxonomia (vocabulario)
    vocab=list()
    with open(tax, 'r') as file: #csv donde vienen la lista del vocabulario (issues)
        csvreader = csv.reader(file)
        for i in csvreader:
            #print(i[8]) # columna de issues
            vocab.append(i[8])
    #print(vocab)
    return vocab  


def search_term_in_sent(table1, vocab): #funcion para buscar termino de la taxonomia en la sentencia
    table2=list()
    train_data=list()
    for i in table1:
        sent=i[1]
        for j in vocab:
            if(j.lower() in sent.text.strip().lower()):
                #print(j.lower())     
                start=sent.text.strip().lower().find(j.lower())
                end=start+len(j)
                #print(start, end)
                if(start != 0):
                    table2.append([i[0],sent.text.strip().lower(),j.lower(), start, end])
                    #train_data.append([(sent.text.strip().lower(),{'entities':[(start, end, j.lower())]})])
                    tupla={'entities':[[start, end, 'issue']]}
                    train_data.append([sent.text.strip().lower(), tupla])      
    print(len(table2),len(train_data))
    with open('issues.json', 'w') as f:
        json.dump(train_data, f)
    #print(train_data)
    return train_data


def search_term_in_text(corpus, vocab): #funcion para buscar termino de la taxonomia en todo el texto
    table2=list()
    train_data=dict()
    #train_data={"annotations", table2 }
    #print(train_data)
    
    for j in vocab:
        if(j.lower() in corpus.strip().lower()):
            #print(j.lower())     
            start=corpus.strip().lower().find(j.lower())
            end=start+len(j)
            #print(start, end)
            if(start != 0):
                print(j)
                table2.append([start, end, 'issue'])
                #train_data.append([(corpus.text.strip().lower(),{'entities':[(start, end, j.lower())]})])
    tupla={'entities':table2}
    train_data={"annotations": [[corpus.strip().lower(), tupla] ]}      
    print(len(table2),len(train_data))
    with open('issues_all_text.json', 'w') as f:
        json.dump(train_data, f)
    #print(train_data)
    
    return train_data


def training(train_data, test):
    
    # inicializar un modelo espacial en blanco
    nlp = spacy.blank('en')
    # Crear un reconocedor de entidades en blanco y añadirlo a la canalización
    ner = nlp.create_pipe('ner')
    ner.add_pipe('ner')
    # Añadir una nueva etiqueta para el lenguaje de programación
    ner.add_label('PROG')
    # Comienza el entrenamiento
    nlp.begin_training()
    # Tren para 10 iteraciones
    for itn in range(10):
        random.shuffle(train_data)
        losses = {}
        # Dividir los ejemplos en lotes
        for batch in spacy.util.minibatch(train_data, size=2):
            for text, annotation in batch:
                # create Example
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotation)
                # Update the model
                nlp.update([example],losses=losses,  drop=0.3)
        print("Losses", losses)

#parte buena
table=ner1('corpus_aiact.csv')
vocab=read_my_vocabulary('vocab.csv')
#train_data=search_term_in_sent(table, vocab)



#test='But what if those who work together in teams now also merge the citizen’s data to form profiles – is that a breach of privacy, or rather the extension of a cooperative approach?'

test=str()
with open('corpus_final.csv', 'r') as file: #csv donde vienen los datos
        csvreader = csv.reader(file)
        for i in csvreader:
            clean=re.sub(r'[^\w\s]+','',i[7])
            clean.replace('\n','')
            if(clean[:-1]=='\n'):
                test+=clean[:-1]
            else:
                test+=clean
#print(test)
train_data=search_term_in_text(test, vocab)       
training(train_data, test)

