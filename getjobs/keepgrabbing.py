from datetime import datetime
from itertools import zip_longest
import json
from urllib.parse import urljoin
import os
from os.path import join
import re
#from multiprocessing import Pool
#from subprocess import Popen, PIPE


import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

import os
#replace save path on server
SQLALCHEMY_DATABASE_URI = os.path.join('C:\\Users\\llinhan\\Documents\\x\\flaskapp_2', 'app.db')

import sqlite3
conn = sqlite3.connect(SQLALCHEMY_DATABASE_URI, timeout = 60)

d = conn.cursor()
d.execute('DELETE FROM job')
conn.commit()

def kpmg():
    
    c = conn.cursor()
    id_count = c.execute('SELECT max(id) FROM job')
    max_id = id_count.fetchone()[0]
    
    seq_id = max_id if max_id else 0
    
    kpmg_list = []
    kpmg_pre_url = 'https://www.kpmg.com.my/KARSFR/'
    kpmg_url = urljoin(kpmg_pre_url,'candViewAd.aspx')
    
    kpmg_job_url = 'https://www.kpmg.com.my/KARSFR/candAdDetails.aspx?AdvertID={}'

    try:
        r = requests.get(kpmg_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to {}".format(kpmg_url))
        print(e)

    soup = BeautifulSoup(r.content, 'lxml')
    
    
    for r in soup.find('table', id = 'MyGrid').find_all('tr')[1:]:
        seq_id += 1
        content = r.find_all('font')
            
            #dates = [i.next_sibling for i in content[0].find_all('b')]
            #ref = content[4].text
        location = content[5].text.strip()
        department = content[6].text.strip()
        title = content[2].find('b').text.strip()
        link = kpmg_job_url.format(content[2].find('a')['onclick'].split("'")[1].split('=')[-1].strip())

        kpmg_list.append((seq_id,'KPMG',title, location, department, link, datetime.utcnow()))
        
    c.executemany('INSERT INTO job VALUES (?,?,?,?,?,?,?)', kpmg_list)
    conn.commit()
    
def deloitte():

    c = conn.cursor()
    id_count = c.execute('SELECT max(id) FROM job')
    max_id = id_count.fetchone()[0]
    
    seq_id = max_id if max_id else 0
    
    deloitte_list = []
    session = HTMLSession()
    r = session.get('https://jobs2.deloitte.com/my/en/')
    r.html.render(wait = 1, sleep = 1)

    urls = r.html.find('#cookieClick > div.ph-page > div > div.container > div.category-slider > section > div > div > div > div.content-block > div > div.au-target.row.category-column-3.category-list-view > div')
    deloitte_urls = [url.find('a', first = True).attrs['href'] for url in urls]

    for url in deloitte_urls:

        try:
            job_session = HTMLSession()
            descs = job_session.get(url)
            descs.html.render(wait = 1, sleep = 1)

            job_descs = descs.html.find('body > div.ph-page > div > div.container > div > div.col-md-8.col-sm-7 > section:nth-child(1) > div > div > div > div.phs-jobs-list > div.phs-jobs-block.au-target > ul > li')
        
            for job in job_descs:
                seq_id += 1
                title = job.find('li > div > a', first = True).attrs['data-ph-at-job-title-text']
                link = job.find('li > div > a', first = True).attrs['href']
                location = job.find('div > a > div > span.job-location', first = True).text
                department = job.find('div > a > div > span.job-category.au-target', first = True).text

                deloitte_list.append((seq_id,'Deloitte',title, location, department, link, datetime.utcnow()))
                
        except requests.exceptions.RequestException as e:
            print("An exception occured while connecting to {}".format(url))
            print(e)

    c.executemany('INSERT INTO job VALUES (?,?,?,?,?,?,?)', deloitte_list)
    conn.commit()       

def ey():

    c = conn.cursor()
    id_count = c.execute('SELECT max(id) FROM job')
    max_id = id_count.fetchone()[0]
    
    seq_id = max_id if max_id else 0

    ey_list = []
    ey_pre_url = 'https://eygbl.referrals.selectminds.com/experienced-opportunities/jobs/search/36000911/'
    ey_urls = [ey_pre_url]

    session = HTMLSession()
    r = session.get(ey_pre_url)
    r.html.render(wait = 1, sleep = 1)

    urls = r.html.find('#jPaginationHldr > div > a')[:-1]
    max_page_no = max([int(url.find('a', first = True).attrs['href'].replace('#page','')) for url in urls])
    ey_urls.extend([urljoin(ey_pre_url,'page{}'.format(no)) for no in range(2,max_page_no+1)])

    for url in ey_urls:

        try:
            job_session = HTMLSession()
            descs = job_session.get(url)
            descs.html.render(wait = 1, sleep = 1)

            job_descs = descs.html.find('#job_results_list_hldr > div.job_list_row')
        
            for job in job_descs:
                seq_id += 1
                title = job.find('div > div.jlr_title > p:nth-child(2)', first = True).text
                link = job.find('div > div.jlr_title > p:nth-child(2) > a', first = True).attrs['href']
                location = job.find('div > div.jlr_title > p:nth-child(3) > span.location', first = True).text
                department = job.find('div > div.jlr_title > p:nth-child(4) > span.category', first = True).text

                ey_list.append((seq_id,'EY',title, location, department, link, datetime.utcnow()))

        except requests.exceptions.RequestException as e:
            print("An exception occured while connecting to {}".format(url))
            print(e)

    c.executemany('INSERT INTO job VALUES (?,?,?,?,?,?,?)', ey_list)
    conn.commit()    

def pwc():

    def pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    c = conn.cursor()
    id_count = c.execute('SELECT max(id) FROM job')
    max_id = id_count.fetchone()[0]

    seq_id = max_id if max_id else 0

    pwc_list = []
    pwc_pre_url = 'https://www.pwc.com/my/en/careers/'
    pwc_url = urljoin(pwc_pre_url,'jobpostings.html')

    _link ='https://www.applytopwc.com/hrpr/publiclogin_malaysia.jsp' 

    try:
        session = HTMLSession()
        r = session.get(pwc_url)
        r.html.render(wait = 1, sleep = 1)

        jobs = r.html.find('#content-free-1-ede2 > div > div.tabsnew.section > div > div')

        for job in jobs:
            link = _link
            location = 'Anywhere'
            department = job.find('div.tabs-new__tab-title-print', first = True).text
            category = [i.text for i in job.find('div > div > div > p')]
            position = [i.text for i in job.find('div > div > div > ul')]
            titles = [' - '.join(i) for i in zip_longest(category, position, fillvalue = '')]
            for title in titles:
                seq_id += 1
                pwc_list.append((seq_id,'PWC',title, location, department, link, datetime.utcnow()))


    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to {}".format(pwc_url))
        print(e)

    c.executemany('INSERT INTO job VALUES (?,?,?,?,?,?,?)', pwc_list)
    conn.commit()   

''' 
    for r in soup.find_all('div', {'class':'tab-content'}):

        jobs = [' - '.join([job.text,job.findNext('li').text]) for job in r.find_all('b')]
        
    for job in jobs:
        print(job)
'''
        #pwc_list.append((seq_id,'PWC',title, location, department, link, datetime.utcnow()))

    #c.executemany('INSERT INTO job VALUES (?,?,?,?,?,?,?)', pwc_list)
    #conn.commit()  

if __name__ == '__main__':
    #loop through functions
    kpmg()
    print('kpmg done')
    deloitte()
    print('deloitte done')
    ey()
    print('ey done')
    pwc()
    print('pwc done')
    conn.close()