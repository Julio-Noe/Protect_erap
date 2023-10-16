
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
import os.path
list_issuesAIAAIC=list()  
issue_list=list()

def temporal_list_articles(working_dir):
    #temporal_path = working_dir + "/corpus_protect/en3/DATABAS.txt"
    temporal_path = working_dir + "/corpus_protect/en3/BLANK.txt"
    list_urls = list()
    temporal_file = open(temporal_path, 'r')
    list_urls = temporal_file.readlines()
    return list_urls



def get_repository_list(url_main):
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
    #Negative numbers mean that you count from the right instead of the left. So, list[-1] refers to the last element, list[-2] is the second-last, and so on.
    #print(bloque[-2])
    #for ul in bloque[-2]:
    for ul in bloque:
        bloque_ul=ul.find_all('a', class_='XqQF9c', href=True) #search all links where are the documents refers to issue
        
        for a in bloque_ul:
            href = a['href']
            if 'http' in href and 'pdf' not in href:
                list_urls.append(a['href'])
    return list_urls

def get_metadata(url):
    if url:
        print(url)
        response1 =urllib.request.urlopen(url)
        html1=BeautifulSoup(response1, 'html.parser')
        issue=str()
        title=str()
        content = str()
        technology=str()
        purpose=str()
        country=str()
        content_list=list()
        content_counter = 0
        #Get title and content
        for article in html1.find_all('div',{'class':'JNdkSc-SmKAyb LkDMRd'}):
            #0 = title
            if content_counter == 0:
                title = article.text
                print("Title: ", title)
            elif content_counter == 3:
                paragraph_list = article.find_all('p')
                for paragraph in paragraph_list:
                    content_list.append(paragraph.text.strip())
                #content = article.text
                print("Content: ", content_list)
                #break
            elif content_counter == 4:
            #elif article.text.find('Country: ') != -1:
                article_text= article.text
                begin_index = article_text.find('Country:')
                end_index = article_text.find('Sector:')
                country = article_text[begin_index+8:end_index].strip()
                print("Country: ",country)
                begin_index = article_text.find('Purpose:')
                end_index = article_text.find('Technology:')
                purpose = article_text[begin_index+9:end_index].strip()
                print("Purpose: ", purpose)
                begin_index = end_index
                end_index = article_text.find('Issue:')
                technology = article_text[begin_index+11:end_index].strip()
                print("Technology: ",technology)
                begin_index = end_index
                end_index = article_text.find('Transparency:')
                issue = article_text[begin_index+7:end_index].strip()
                print("Issue: ",issue)
                if(issue not in list_issuesAIAAIC):
                    list_issuesAIAAIC.append(issue)
            if content_counter > 5:
                break
            content_counter += 1       
        return(title, issue, technology, purpose, country, content_list)

def get_text_link(url, issue):
    document_counter=1
    issue_list = issue.split(';')
    text_list=list()
    
    
    for issue in issue_list:
        if('/' in issue):
            issue_splited=issue.split('/')
            issue=issue_splited[0]
    
    if(url):
        #print('---->',url)
        try:
            blacklist=['https://www.sacbee.com/news/nation-world/national/article252604333.html','https://amp.miamiherald.com/news/local/community/florida-keys/article230945733.html','https://www.flkeysnews.com/news/local/article230945733.html']
            if((url in blacklist) ):
                print('nothing to do in: ', url)
            elif('.pdf' in url[-4:]):
                print('nothing to do; it is a pdf file')
            
            else:
                if(url not in blacklist):
                    #print('entra try')
                    print("link: ", url)
                    response= requests.get(url, timeout = 5)
                    #print(response)
                    html=BeautifulSoup(response.text, 'html.parser')
                    results=html.find_all('p', text=True)
                    #print(results)
                    response.raise_for_status()

                    for result in results:
                        name = result.get_text()
                        raw_text=''.join(name)
                        text_list.append(raw_text+'\n')               
                    document_counter=document_counter+1
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
                raw_text=''.join(name)
                text_list.append(raw_text.strip())
                #file1.write(t+'\n')
            pass
        except ValueError as e:
            print()
            print("Value error 4")
            pass
        except:
            pass
    return text_list

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
                    issue_list.append(iss.strip())     
            

            elif('-' in i):
                issue_l2=i.split('-')
                #print('issue 2 ', issue_l2)
                for iss in issue_l2:
                    #print( iss)
                    issues.append(iss.strip())
                    issue_list.append(iss.strip())
            else:
                issues.append(i.strip())
                issue_list.append(i.strip())
    elif len(issue_bad) > 0:
        issues.append(issue_bad.strip())
        issue_list.append(issue_bad.strip())
    print(issues)
    return issue_list, issues
    #return '; '.join(str(x) for x in issues)

def strip_nonalnum_re(word):
    return re.sub(r"^\W+|\W+$", "", word)