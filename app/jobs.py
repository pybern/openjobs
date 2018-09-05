from collections import namedtuple
from datetime import datetime
import json
from urllib.parse import urljoin
import os
from os.path import join
import re

import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from multiprocessing import Pool
from subprocess import Popen, PIPE

import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

#replace save path on server
JSON_PATH = join('C:/Users/llinhan/Documents/x/flaskapp/','data/json/')

def kpmg():

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
            content = r.find_all('font')
            
            #dates = [i.next_sibling for i in content[0].find_all('b')]
            #ref = content[4].text
            location = content[5].text.strip()
            department = content[6].text.strip()
            title = content[2].find('b').text.strip()
            link = kpmg_job_url.format(content[2].find('a')['onclick'].split("'")[1].split('=')[-1].strip())

            kpmg_list.append((title, location, department, link))

    for 


