import spacy
import csv
import re
import pandas as pd
import random
import json
from spacy.training.example import Example
from spacy.util import minibatch, compounding
from pathlib import Path
from spacy.language import Language
from langdetect import detect
#nlp = spacy.load("en_core_web_lg")
# Getting the pipeline component
#ner=nlp.get_pipe("ner")
'''
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
    '''

def create_table_id_text(doc): #funcion para obtener tabla con [idnumerodoc_numerosentencia, sentencia]
    nlp = spacy.load("en_core_web_lg")
    table1=list()
    test=str()
    with open(doc, 'r') as file: #csv donde vienen los datos
        csvreader = csv.reader(file)
        for i in csvreader:
            clean = re.sub(r'[^\w\s]+','',i[7])
            clean=clean.replace('\n', '')
            test+=clean
            document = nlp(clean)
            table1.append([i[0], clean])
    #for i in table1:
    #    print(i)
    f = open("alldocuments.txt", "a")
    f.write(clean)
    f.close()
    return table1, test
    
                    
def read_my_vocabulary(tax, column): #funcion para leer la propia taxonomia (vocabulario)
    vocab=list()
    with open(tax, 'r') as file: #csv donde vienen la lista del vocabulario (issues)
        csvreader = csv.reader(file)
        for i in csvreader:
            #print(i[8]) # columna de issues
            vocab.append(i[column-1].lower())
            
    
    print(vocab[7:])
    return vocab[7:]  

def search_term_in_document(doc, vocab): #funcion para buscar termino de la taxonomia en la sentencia
    table2=list()
    train_data=list()
    with open(doc, 'r') as file: #csv donde vienen los datos
        csvreader = csv.reader(file)
        for i in csvreader:
            doc_clean = re.sub(r'[^\w\s]+','',i[7])
            for j in vocab:
                if(j.lower() == doc_clean.strip().lower()):
                    #print(j.lower())     
                    start=doc_clean.strip().lower().find(j.lower())
                    end=start+len(j)
                    if(start != 0):
                        #table2.append([i[0],doc.text.strip().lower(),j.lower(), start, end])
                        #train_data.append([(doc.text.strip().lower(),{'entities':[(start, end, j.lower())]})])
                        tupla={'entities':[[start, end, 'issue']]}
                        
                        train_data.append([doc_clean.strip().lower(), tupla])      
    print(train_data)
    train_data2={"annotations": train_data}   
    print(len(table2),len(train_data2))
    with open('annotation_by_document.json', 'w') as f:
        json.dump(train_data2, f)
    #print(train_data)
    return train_data2

def search_term_in_sent(table1, vocab): #funcion para buscar termino de la taxonomia en la sentencia
    table2=list()
    train_data=dict()
    sents=list()
    tupla=list()
    
    for i in table1:
        sent=i[1].strip().lower()
        #print(sent, type(sent))
        separete_sent=sent.split(' ')
        entities=list()
        for j in vocab:
            #print('----',sent.find(j), j)
            if(sent.find(j) != -1):
                found=sent.find(j)
                finish_found=found+len(j)
                j_low=j.lower()
                print('encontrado',found, finish_found, '-->',j_low)
                entities_dict=dict()
                entities_dict['entities']=entities
                #sents.append([sent.strip().lower(), entities_dict])    
                #start=sent.strip().lower().find(j.lower())
                #end=start+len(j)  
                if(found > 0):
                    print('here')
                    entities.append([found, finish_found, 'issue'])
        if(len(entities)>0):
            tupla.append([sent.strip().lower(), entities_dict])
 
        
    train_data["annotations"]= tupla
    print(train_data)
    with open('anotation_by_link.json', 'w') as f:
        json.dump(train_data, f)
    
    return #train_data2


def search_term_in_text(corpus, vocab): #funcion para buscar termino de la taxonomia en todo el texto
    table2=list()
    train_data=dict()
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
table=create_table_id_text('corpus_by_link_test.csv') #se forma una tabla [ide, sentence]
vocab=read_my_vocabulary('vocab.csv', 9)#se forma una columna solo del vocabulario.

#table=[['1', 'hola como estas'],['2', ' 1 hola como estas gdf'],['11', ' 2 hola como estas tfe'],['12', '3 hola como estas fjwe' ],['13', '4 hola como estas ew'],['15', '5 hola como estas ewr'],['18', '6 hola como estas'],['19', '7 hola como estas erwer']]
#vocab=['hola', 'estas', 'tfe']
train_data=search_term_in_sent(table[0], vocab) #corpus json por oraciones
#search_term_in_document('corpus_final.csv', vocab)
#test='But what if those who work together in teams now also merge the citizen’s data to form profiles – is that a breach of privacy, or rather the extension of a cooperative approach?'
'''
test=str()#test es todo el texto plano del corpus
with open('corpus_final.csv', 'r') as file: #csv donde vienen los datos
    csvreader = csv.reader(file)
    print(csvreader)
    n=0
    for i in csvreader:
        clean=re.sub(r'[^\w\s]+','',i[7])
        clean.replace('\n','')
        test+=clean
        print(clean)
        n=n+1
#print(test)'''
#train_data=search_term_in_text(table[1], vocab)   #funcion para buscar termino de la taxonomia en todo el texto    
#training(train_data, test) #entrenamiento

