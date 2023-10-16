import spacy
import csv
import re
import pandas as pd
import random
import json
import os
from spacy.training.example import Example
from spacy.util import minibatch, compounding
from pathlib import Path
from spacy.language import Language
from langdetect import detect
from nltk.stem import WordNetLemmatizer
from regex import finditer
import corpus_functions as cp


print("loading dataset...")
working_dir = os.getcwd() + '/AIAAIC corpus'
#Create table [id, sentence]
table = cp.create_table_id_text(working_dir+'/corpus_final.csv') 
print("dataset loaded")

vocab = cp.read_my_vocabulary('/vocab.csv', 9)#se forma una columna solo del vocabulario.
#vocab = cp.read_my_ai_vocabulary('./ai_act_list_concepts')

#train_data = cp.search_term_in_sent(table[0], vocab) #corpus json por oraciones

cp.training_data_generation_by_sentence(table[0], vocab) #corpus json por oraciones

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

