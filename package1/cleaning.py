#!/usr/bin/env python
# coding: utf-8

# In[3]:

import pandas as pd
import os
import numpy as np
from sqlalchemy import create_engine

def drop_cols_threshold (table, n):
    threshold = n
    null_cols = table.isnull().sum()
    null_cols = null_cols[null_cols > 0] / len(table) * 100
    null_filter = null_cols > threshold
    drop_cols = list(null_cols[null_filter].index)
    table_clean = table[[x for x in table.columns if x not in drop_cols]]
    return table_clean


def clean(eng):

    business_info = pd.read_sql_table('business_info', con=eng)
    personal_info = pd.read_sql_table('personal_info', con=eng)
    rank_info = pd.read_sql_table('rank_info', con=eng)
    
    
    business_info_clean = drop_cols_threshold (business_info, 40) 
    business_info_clean= business_info_clean.drop(['Unnamed: 0'], axis=1)
    business_info_clean[['business category ','company name']] = business_info_clean.Source.str.split(" ==> ",expand=True)
    business_info_clean.drop(columns =["Source"], inplace = True) 
    
    personal_info_clean = drop_cols_threshold(personal_info, 40) 
    personal_info_clean = personal_info_clean.drop(['Unnamed: 0'], axis=1)
    personal_info_clean['gender'] = personal_info_clean['gender'].str.replace('Male', 'M')
    personal_info_clean['gender'] = personal_info_clean['gender'].str.replace('Female', 'F')
    personal_info_clean['lastName'] = personal_info_clean['lastName'].str.capitalize() 
    personal_info_clean['age'] = personal_info_clean['age'].str.replace(' years old', '')
    personal_info_clean['age'] = personal_info_clean['age'].fillna(-1)
    personal_info_clean['age'] = personal_info_clean['age'].astype(int)
    personal_info_clean['age'] = personal_info_clean['age'].apply(lambda x: 2020-x if x > 200 else x)
    personal_info_clean['age'] = personal_info_clean['age'].astype(str)
    personal_info_clean['age'] = personal_info_clean['age'].replace('-1', np.nan)
    
    
    rank_info_clean = drop_cols_threshold(rank_info, 40) 
    rank_info_clean = rank_info.drop(['Unnamed: 0'], axis=1)
    rank_info_clean['name'] = rank_info_clean['name'].str.capitalize() 
    rank_info_clean['position'].round(0)
    
    forbes_info=pd.merge(business_info_clean, personal_info_clean, on='id')
    forbes_info=pd.merge(forbes_info, rank_info_clean, on='id')
    forbes_info=forbes_info[['id', 'realTimePosition', 'name', 'lastName', 'gender', 'age', 'country', 'business category ', 'company name', 'worth', 'worthChange', 'image']]

    output_folder = 'processed'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    forbes_info.to_csv(f'{output_folder}/Billionaires_clean.csv', index=False)

    return forbes_info

