import json
from urllib.parse import urljoin
import os
from os.path import join
import re

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from collections import OrderedDict
from multiprocessing import Pool
from subprocess import Popen, PIPE

#replace save path on server
JSON_PATH = join('C:/Users/llinhan/Documents/x/flaskapp_2/','data/json/')

def kpmg():

    kpmg_dict = OrderedDict()
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
            content = r.find_all('font')
            
            #dates = [i.next_sibling for i in content[0].find_all('b')]
            #ref = content[4].text
            #location = content[5].text
            #department = content[6].text
            
            job = content[2].find('b').text
            id = content[2].find('a')['onclick'].split("'")[1].split('=')[-1]

            kpmg_dict[job] = kpmg_job_url.format(id)

    return kpmg_dict

def pwc():

    pwc_dict = OrderedDict()
    pwc_pre_url = 'https://www.pwc.com/my/en/careers/'
    pwc_url = urljoin(pwc_pre_url,'jobpostings.html')

    try:
        r = requests.get(pwc_url)
    except requests.exceptions.RequestException as e:
        print("An exception occured while connecting to {}".format(pwc_url))
        print(e)

    soup = BeautifulSoup(r.content, 'lxml')

    for r in soup.find_all('div', {'class':'tab-content'}):
        jobs = [' - '.join([job.text,job.findNext('li').text]) for job in r.find_all('b')]
        
    for job in jobs:
        pwc_dict[job] ='https://www.applytopwc.com/hrpr/publiclogin_malaysia.jsp' 

    return pwc_dict
        
def deloitte():

    deloitte_dict = OrderedDict()

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
                title = job.find('li > div > a', first = True).attrs['data-ph-at-job-title-text']
                link = job.find('li > div > a', first = True).attrs['href']
                location = job.find('div > a > div > span.job-location', first = True).text
                department = job.find('div > a > div > span.job-category.au-target', first = True).text
                deloitte_dict[title] = link
                print(title, location, department)
        except requests.exceptions.RequestException as e:
            print("An exception occured while connecting to {}".format(url))
            print(e)

    return deloitte_dict

def ey():

    ey_dict = OrderedDict()
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
                title = job.find('div > div.jlr_title > p:nth-child(2)', first = True).text
                link = job.find('div > div.jlr_title > p:nth-child(2) > a', first = True).attrs['href']
                ey_dict[title] = link

        except requests.exceptions.RequestException as e:
            print("An exception occured while connecting to {}".format(url))
            print(e)

    return ey_dict



#gotta fixed duplicate job names

if __name__ == '__main__':
    with open(join(JSON_PATH,'data.json'), "w") as out:
        json.dump({'KPMG':kpmg(),'PWC':pwc(), 'Deloitte':deloitte(), 'EY':ey()}, out)