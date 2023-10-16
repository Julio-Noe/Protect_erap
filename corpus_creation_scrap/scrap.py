
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from jinja2 import is_undefined
from nltk import tokenize
from nltk.tokenize import word_tokenize
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from urllib.request import urlopen
import csv
import os
import string
import functions #local functions

#Paths definition
working_dir = os.getcwd() + '/corpus_creation_scrap'
print(working_dir)
in_corpus_path = working_dir + '/corpus_protect/en3/in_corpus.txt'
issues_aiaaic_path = working_dir + '/corpus_protect/en3/issues_AIAAIC.txt'
paragraph_issue_path = working_dir + '/corpus_protect/en3/paragraph_issue.txt'
corpus_path = working_dir + '/corpus_protect/en3/corpus_final.csv'
#Files manipulation
fc=open(in_corpus_path,'a')
iss=open(issues_aiaaic_path, 'w')
paragraph_issue_file=open(paragraph_issue_path, 'a')

if os.path.exists(corpus_path):
    corpus_file=open(corpus_path, 'a', newline='')
    writer_corpus_csv = csv.writer(corpus_file)
else:
    corpus_file=open(corpus_path, 'w', newline='')
    writer_corpus_csv = csv.writer(corpus_file)
    writer_corpus_csv.writerow(['ID','AIAAIC Link','Related link', 'AIAAIC Article Title', 'Technology', 'Purpose', 'Issues', 'Country','Text'])

# URL of the AIAAIC (AI, algorithmic, and automation incidents) list of articles 
url_repo= "https://www.aiaaic.org/aiaaic-repository/ai-algorithmic-and-automation-incidents" 

# List of problematic URLS - contain not UTF-8 characters
black_list=['https://www.aiaaic.org/aiaaic-repository/ai-algorithmic-and-automation-incidents/são-geraldo-magela-drone-delivery','https://www.aiaaic.org/aiaaic-repository/ai-algorithmic-and-automation-incidents/viogén-gender-violence-system','https://www.aiaaic.org/aiaaic-repository/ai-algorithmic-and-automation-incidents/buenos-aires-sistema-de-reconocimiento-facial-de-prófugos','Engineer.ai misleading marketing','https://www.aiaaic.org//aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/são-geraldo-magela-drone-delivery', 'https://www.aiaaic.org//aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/viogén-gender-violence-system','https://www.aiaaic.org//aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/dall-e-image-generation-bias-stereotyping','https://www.aiaaic.org//aiaaic-repository','https://www.stuff.co.nz/motoring/300572609/video-captures-driverless-tesla-crashing-into-us3-million-private-jet','ValueError: unknown url type:','MoviePass 2.0 PreShow eye tracking','Pony.ai driverless test crash','Gdansk Primary School No. 2 meal payment verification', 'https://www.aiaaic.org/aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/berlin-südkreuz-rail-station-algorithmic-surveillance','https://www.aiaaic.orghttps://drive.google.com/open?id=1GkLO9BhqOp-JCm3pXpSJyyhJWty4P4XCwO4N4LjZ-jI','https://www.aiaaic.org/aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/viogén-gender-violence-system','https://www.aiaaic.org/aiaaic-repository/ai-and-algorithmic-incidents-and-controversies/são-geraldo-magela-drone-delivery']

# get the list of articles from the AIAAIC dataset
#list_repo=functions.get_repository_list(url_repo)
list_repo = functions.temporal_list_articles(working_dir)

matrix_repo=list()

for i in list_repo:
    matrix_repo.append([i, []])

documents_text=list()
list_paragraph=list()
all_files = len(matrix_repo)
url_counter=1 
counter = 0
for url_m in matrix_repo:
    print("=============",counter,"-",all_files,"============")
    #counter = counter + 1
    """"   
    if counter > 25:
        break
    """
    raw_url=url_m[0].encode('utf-8')#url repo nivel 2
    url=raw_url.decode('utf-8')
    
    # Save URLs processed (avoid start again the process)
    in_corpus_read = open(in_corpus_path,'r')
    
    in_corpus_lines=in_corpus_read.readlines()
    if(url+'\n' in in_corpus_lines):
        pass
    else:
        counter = counter + 1
        if((url not in black_list) ):
            fc.write(url+'\n')
            #print('-->',url)
            # Get metadata (box)
            article_metadata=functions.get_metadata(url) 
            title = article_metadata[0]
            issue = article_metadata[1]
            technology = article_metadata[2]
            purpose = article_metadata[3]
            country = article_metadata[4]
            content_list = article_metadata[5]
            l_issues=functions.separate_issues(issue)
            
            if len(l_issues[1]) > 1:
                l_issues_join='; '.join(l_issues[1])
            else:
                l_issues_join = ''.join(l_issues[1])
                print(l_issues_join)
            url_links_list=functions.repository_issues(url) #Links list of News, commentary, analysis
            
            if len(content_list) > 0:
                for content in content_list:
                    text_al = functions.strip_nonalnum_re(content)
                    for j in tokenize.sent_tokenize(text_al):
                        printable_text = ''.join([str(char) for char in j if char in string.printable])
                        writer_corpus_csv.writerow([ str(url_counter)+'_0', url, url, title, technology.replace(';','|'), purpose, l_issues_join, country, printable_text.strip()])
        
            paragraph_issue_file.write('Nuevo documento|'+url+'\n')
            print_counter = 1
            links_counter=1
            total_links = len(url_links_list)
            for url_link in url_links_list:
                print('Processing link: ', print_counter," of ", total_links)
                print_counter += 1

                url_m[1].append(url_link)
                listlinks='; '.join(url_m[1])
                text_list=functions.get_text_link(url_link, issue)
                if text_list != "" or len(text_list) > 0:
                    documents_text.append(' '.join(text_list))
                    partial_result_file=open(working_dir+'/corpus_protect/en3/corpus_BLANK_'+str(url_counter)+'_'+str(links_counter)+'.txt', 'a')
                    partial_result_file.write('AIAAIC link: '+url+'\n')
                    partial_result_file.write('Related link: '+url_link+'\n')
                    partial_result_file.write('Title: '+title+'\n')
                    partial_result_file.write('Technology: '+technology+'\n')
                    partial_result_file.write('Purpose: '+purpose+'\n')
                    partial_result_file.write('Issue: '+l_issues_join+'\n')
                    partial_result_file.write('------'+'\n')
                    url_link_text=''.join(' '.join(text_list))
                    partial_result_file.write(url_link_text)
                    write_file = False
                    for text in text_list:
                        text_al = functions.strip_nonalnum_re(text)
                        if len(text_al) > 100:
                            for j in tokenize.sent_tokenize(text_al):
                                printable_text = ''.join([str(char) for char in j if char in string.printable])
                                writer_corpus_csv.writerow([ "BLANK_"+str(url_counter)+'_'+str(links_counter), url, url_link, title, technology.replace(';','|'), purpose, l_issues_join, country, printable_text.strip()])#se escribe en formato csv
                                write_file = True
                if write_file:
                    links_counter += 1 
            url_counter=url_counter+1

