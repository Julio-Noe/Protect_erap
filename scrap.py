
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from urllib.error import HTTPError
from jinja2 import is_undefined
import requests
import spacy
import nltk
from nltk.tokenize import word_tokenize
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import json
from urllib.request import urlopen
import re
import os
import csv
import functions #aqui estan las funciones
#import word2vect_code

fc=open('corpus_protect/1/in_corpus.txt', 'a')
iss=open('corpus_protect/1/issues_AIAAIC.txt', 'w')
gold=open('corpus_protect/1/paragraph_issue.txt', 'a')
url_repo= "https://www.aiaaic.org/aiaaic-repository/ai-and-algorithmic-incidents-and-controversies" #access to main web of database AI
no=['Engineer.ai misleading marketing','https://www.aiaaic.org//aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/são-geraldo-magela-drone-delivery', 'https://www.aiaaic.org//aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/viogén-gender-violence-system','https://www.aiaaic.org//aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/dall-e-image-generation-bias-stereotyping','https://www.aiaaic.org//aiaaic-repository','https://www.stuff.co.nz/motoring/300572609/video-captures-driverless-tesla-crashing-into-us3-million-private-jet','ValueError: unknown url type:','MoviePass 2.0 PreShow eye tracking','Pony.ai driverless test crash','Gdansk Primary School No. 2 meal payment verification', 'https://www.aiaaic.org/aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/berlin-südkreuz-rail-station-algorithmic-surveillance','https://www.aiaaic.orghttps://drive.google.com/open?id=1GkLO9BhqOp-JCm3pXpSJyyhJWty4P4XCwO4N4LjZ-jI','https://www.aiaaic.org/aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/viogén-gender-violence-system','https://www.aiaaic.org/aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/são-geraldo-magela-drone-delivery']



list_repo=functions.repository_list(url_repo)
matrix_repo=list()
for i in list_repo:
    matrix_repo.append([i, []])

file=open('corpus_protect/1/corpus_final.csv', 'w', newline='')
writer_csv = csv.writer(file)
writer_csv.writerow(['NAME_DOC','REPO_LEVEL(2)','LIST_LINKS', 'TITLE', 'TECHNOLOGY', 'PURPOSE', 'ISSUES', 'TEXT'])
texto_documents=list()
n_url=1 
list_paragraph=list()
for url_m in matrix_repo:
    ur=url_m[0].encode('utf-8')#url repo nivel 2
    url=ur.decode('utf-8')
    fr = open('corpus_protect/1/in_corpus.txt','r')#aqui se guardan cada una de la informacion
    filer=fr.readlines()
    
    if(url+'\n' in filer):
        pass
    else:
        if((url not in no) ):
            fc.write(url+'\n')
            print('-->',url)
            info=functions.get_info(url) #se obtiene la informacion de la caja de metadatos.
            title=info[0]
            issue=info[1]
            tech=info[2]
            purpose=info[3]
            l_issues=functions.separate_issues(issue)
            l_issues_join='; '.join(l_issues[1])
            list_repo2=functions.repository_issues(url) #Links list of News, commentary, analysis
           
        
            gold.write('Nuevo documento|'+url+'\n')
            n_=1
            n=1
            for url2 in list_repo2:
                url_m[1].append(url2)
                listlinks='; '.join(url_m[1])
                texto=functions.corpus(url2, url,  issue, title, n_, l_issues_join)
                texto_documents.append(texto)
                file1=open('corpus_protect/1/corpus'+str(n_url)+'_'+str(n)+'.txt', 'a')
                file1.write('URL_repo: '+url+'\n')
                file1.write('URL_FILE: '+url2+'\n')
                file1.write('TITULO: '+title+'\n')
                file1.write('TECHNOLOGY: '+tech+'\n')
                file1.write('PURPOSE: '+purpose+'\n')
                file1.write('ISSUE: '+l_issues_join+'\n')
                file1.write('------'+'\n')
                join_texto=''.join(texto)
                file1.write(join_texto)
                writer_csv.writerow([ str(n_url)+'_'+str(n), url, url2, title, tech.replace(';','|'), purpose, l_issues_join,  texto.replace('\n','')])#se escribe en formato csv
    n_url=n_url+1

