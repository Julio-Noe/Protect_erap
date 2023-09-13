
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
list_issuesAIAAIC=list()  
isuue_list=list()
def repository_list(url_main):
    list_urls=list()
    lines_f=list()
    response1 =urllib.request.urlopen(url_main)
    html1=BeautifulSoup(response1, 'html.parser')
    bloque=html1.find_all('ul',{'class':"n8H08c UVNKR"})

    
    for ul in bloque:
        bloque_ul=ul.find_all('li',{'class':'zfr3Q TYR86d eD0Rn'}) #search all links where are the documents refers to issue
        #print(bloque_ul) 
        for urls_ in bloque_ul:
            each_url=urls_.find_all('a', class_='XqQF9c')
            if(len(each_url)>0):
                each_url_0=each_url[0]
                if('.' in each_url_0.text):
                    each_url_0=each_url_0.text
                    if(each_url_0 not in lines_f):
                        list_urls.append(each_url_0)
                elif(each_url_0.has_attr('href')):
                    each_url_0='https://www.aiaaic.org'+each_url_0['href']
                    if(each_url_0 not in lines_f):
                        list_urls.append(each_url_0)
                        lines_f.append(each_url_0)
    
    #print(lines_f[:10])
    return lines_f

def repository_issues(url_main):
    list_urls=list()
    response1 =urllib.request.urlopen(url_main)
    html1=BeautifulSoup(response1, 'html.parser')
    bloque=html1.find_all('ul',{'class':"n8H08c UVNKR"})
    for ul in bloque[-2]:
        bloque_ul=ul.find_all('a', class_='XqQF9c') #search all links where are the documents refers to issue
        

        for j in bloque_ul:
            list_urls.append(j.text)
     
    return list_urls

def get_info(url_main):
    if url_main:
        response1 =urllib.request.urlopen(url_main)
        html1=BeautifulSoup(response1)
        issue=str()
        title=str()
        tech=str()
        purpose=str()
        country=str()
        if(html1.find('h1')!=None):
            title=html1.find('h1').text
        elif(html1.find('strong') !=None):
            title=html1.find('strong').text
        p=html1.find_all("p", {'class':'zfr3Q CDt4Ke'})
        #print('XXXXXXXX',p[0], len(p))
        for i in (html1.find_all("p", {'class':'zfr3Q CDt4Ke'})): #label 'p' is for text, so, search all text in the web
            data=[]
            texto=i.get_text()
            
            
            #print('textoooooo',texto)
            if('Country: ' in texto):
                if('Country: USA' in texto):
                    #print('1-----',texto)
                    start=texto.find('Country: ')
                    getcountry=texto[start+8:]
                    search_end=getcountry.find('Sector:')
                    country=texto[start+8:start+12]
                    print('-----------',country)
                elif('Country: UK' in texto):
                    #print('2-----',texto)
                    start=texto.find('Country: ')
                    getcountry=texto[start+8:]
                    search_end=getcountry.find('Sector:')
                    country=texto[start+8:start+11]
                    print('-----------',country)
               
                    
            elif('Technology: ' in texto):
                start1=texto.find('Technology: ')
                gettech=texto[start1+11:]
                search_end=gettech.find('Issue:')
                tech=gettech[:search_end]
                print('Technology: ',start1,tech)
                if('Issue' in texto):
                    start3=texto.find('Issue:')
                    getissue=texto[start3+7:]
                    search_end=getissue.find('Transparency')
                    issue=getissue[:search_end]
                    print('Issue:',start3,getissue)

            elif('Purpose:' in texto):
                start2=texto.find('Purpose:')
                getpurpose=texto[start2+9:]
                search_end=getpurpose.find('Technology:')
                purpose=getpurpose[:search_end]
                print('Purpose:',start2,getpurpose)
            elif('Issue' in texto):
                print('nooooooooooooooo')
                start3=texto.find('Issue:')
                getissue=texto[start3+7:]
                search_end=getissue.find('Transparency')
                issue=getissue[:search_end]
                print('Issue:',start3,getissue)
                        
                if(issue not in list_issuesAIAAIC):
                    list_issuesAIAAIC.append(issue)
           
                
                
           
        #print(issue,'---------')
        #print('TITLE----------', title)
        return(title, issue, tech, purpose, country)

def corpus(url, repo,  issue, titulo, n_, l_issues):
    n_doc=1
    nlp = spacy.load('en_core_web_md')
    iss=nlp(issue)
    listissue=issue.split(';')
    texto2=list()
    list_text=list()
    in_corpus=list()
    for isu in listissue:
        if('/' in isu):
            isu2=isu.split('/')
            isu=isu2[0]
    
    if(url):
        #print('---->',url)
        try:
            #list_no=['https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9677377', 'https://www.nasdaq.com/articles/six-children-and-one-adult-injured-in-tesla-crash-2021-08-17', 'https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/9675440', 'https://www.gpdp.it/web/guest/home/docweb/-/docweb-display/docweb/9677611', 'https://www.dataguidance.com/news/italy-garante-fines-foodinho-%E2%82%AC26m-unlawful-employee', 'https://www.stuff.co.nz/business/108106220/humans-still-have-final-say-on-almost-all-nz-government-decisions', 'https://www.itv.com/news/meridian/2021-08-16/car-collides-with-pedestrians-in-sussex','https://www.hulldailymail.co.uk/news/celebs-tv/loose-women-share-feelings-hull-4918390','https://www.stuff.co.nz/national/politics/300420063/secretive-facial-recognition-trial-at-wellington-airport-went-against-privacy-commissioners-advice','https://www.stuff.co.nz/technology/digital-living/126691808/privacy-watch-how-to-keep-big-brother-at-bay','https://www.timesofisrael.com/idf-building-facial-recognition-database-of-palestinians-in-hebron-report/','https://www.seattletimes.com/business/rent-going-up-one-companys-algorithm-could-be-why/','https://www.stuff.co.nz/motoring/300572609/video-captures-driverless-tesla-crashing-into-us3-million-private-jet','https://www.coupang.com','https://www.seattletimes.com/business/technology/facial-recognition-lawsuits-against-amazon-and-microsoft-can-proceed-judge-rules/','https://www.stuff.co.nz/entertainment/games/127789184/bbc-investigation-finds-virtual-sex-parties-happening-in-childrens-computer-game-roblox','https://www.kompas.tv/article/272949/newsguard-algoritma-tiktok-suapi-pengguna-dengan-konten-disinformasi-soal-konflik-rusia-ukraina','https://www.miamiherald.com/news/politics-government/state-politics/article256293082.html','https://www.tiktok.com/@miabellaceo/video/7032987655449218309','https://www.tiktok.com/@miabellaceo/video/7032987655449218309','https://www.tiktok.com/@miabellaceo/video/7032987655449218309','https://iapps.courts.state.ny.us/fbem/DocumentDisplayServlet?documentId=rJEK5gDQqtBwJzQw1z8y2g==&system=prod','https://iapps.courts.state.ny.us/fbem/DocumentDisplayServlet?documentId=rJEK5gDQqtBwJzQw1z8y2g==&system=prod']
            list_no=['https://www.sacbee.com/news/nation-world/national/article252604333.html','https://amp.miamiherald.com/news/local/community/florida-keys/article230945733.html','https://www.flkeysnews.com/news/local/article230945733.html']
            if((url in list_no) ):
                print('sin nada')
            elif('.pdf' in url[-4:]):
                print('sin nada')
            
            else:
                if(url not in list_no):
                    #print('entra try')
                    response= requests.get(url, timeout = 2)
                    #print(response)
                    html=BeautifulSoup(response.text, 'html.parser')
                    results=html.find_all('p')
                    #print(results)
                    records = []
                    response.raise_for_status()

                    for result in results:
                        name = result.get_text()
                        t=''.join(name)
                        texto2.append(t+'\n')

                
                    n_doc=n_doc+1
        except HTTPError as e:
            # Need to check its an 404, 503, 500, 403 etc.
            status_code = e.response.status_code
            pass

        except requests.exceptions.HTTPError as err:
            print('not found')
            #raise SystemExit(err)
            pass
        
        except HTTPError as e:
            print()
            print('----ERROR 1-----')
            pass
        except ImportError as e:
            print()
            print('----ERROR 2-----')
            pass
        except TypeError as e:
            print("Type error 3", e)
            response =requests.get(url)
            #print(response)
            html=BeautifulSoup(response.text, 'html.parser')
            results=html.find_all('p')
            for result in results:
                name = result.get_text()
                #print(name)
                t=''.join(name)
                texto2.append(t.strip())
                #file1.write(t+'\n')
            pass
        except ValueError as e:
            print()
            print("Value error 4")
            pass
        except:
            pass
        
        #file1.close()
    texto_str=' '.join(texto2)
    return(texto_str)

def separate_issues(issue_bad):
    #s = re.sub(r'[; ]', '', issue_bad)
    issues=list()
    if(';' in issue_bad):   
        issue_l=issue_bad.split(';')
        for i in issue_l:
            #print('1. ',i)
            if(',' in i):
                issue_l2=i.split(',')
                #print('issue 2', issue_l2)
                for iss in issue_l2:
                    #print( iss)
                    issues.append(iss.strip())
                    isuue_list.append(iss.strip())     
            

            elif('-' in i):
                issue_l2=i.split('-')
                #print('issue 2 ', issue_l2)
                for iss in issue_l2:
                    #print( iss)
                    issues.append(iss.strip())
                    isuue_list.append(iss.strip())
            else:
                issues.append(i.strip())
                isuue_list.append(i.strip())

    return isuue_list, issues
