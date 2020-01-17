#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os 

def smart_parser(row_text):
    row_text = row_text.replace('\nPopulation\n\n\n', '\nPopulation\n').strip('\n')
    row_text = row_text.replace('\n\n', '\n').strip('\n')
    row_text = row_text.replace('\nPopulation\n% of World\n', '\nPopulation % of World\n').strip('\n')
    row_text = re.sub('\[\d\]', '', row_text)
    return list(map(lambda x: x.strip(), row_text.split('\n')))

def scraping(forbes_info):
    
    url='https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all('table',{'class':'wikitable sortable mw-datatable'})[0]
    rows = table.find_all('tr')
    rows_parsed = [row.text for row in rows]
    well_parsed = list(map(lambda x: smart_parser(x), rows_parsed))
    colnames = well_parsed[0]
    data = well_parsed[1:]
    df = pd.DataFrame(data, columns=colnames)
    df['Country(or dependent territory)']=df['Country(or dependent territory)'].replace(['\[(.*?)\]','\(([^\)]+)\)'], ['',''], regex=True)
    df.columns = ['Rank', 'country','Population',' % of World Population','Date','Source']
    forbes_info_result=pd.merge(forbes_info, df, on='country')
    output_folder = 'processed'

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    forbes_info_result.to_csv(f'{output_folder}/Results.csv', index=False)

    return forbes_info_result

# In[ ]:




