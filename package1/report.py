#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def report(forbes_info):
    
    colors = ['burlywood', 'yellowgreen', 'gold', 'r', 'orangered', 'mediumvioletred', 'skyblue', 'navy', 'grey', 'black']
    f = plt.figure()
    forbes_info['company name'].value_counts()[:10].plot(kind='bar', width=0.9, figsize=(20,10), color = colors)
    plt.xlabel('business category (Top 10)')
    plt.ylabel('Toal number of billionaires')
    plt.title('Number of billionaires per country')
    plt.show()
    f.savefig("report.pdf", bbox_inches='tight')
    return fig.savefig('../data/results/results.png')


# In[ ]:




