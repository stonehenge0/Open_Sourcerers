import os
import pandas as pd
from collections import Counter

#   get the relative file name for the grant_data file, provided script and datafile are stored in the same folder
script_dir = os.path.dirname(__file__)
data_filename = "\\grant_data_slim.xlsx"
data_path = script_dir+data_filename

#   get the relative file name for the databank file, provided script and databankfile are stored in the same folder
databank_filename = "\\databank.py"
databank_path = script_dir+databank_filename

#   turn datafile into panda dataframe
df_grant = pd.read_excel(data_path)

      
databank = df_grant.to_dict('records')
DATABANK = {}   # naming guideline for constants is all caps, this will be our databank constant

# trying to trnasfer the Country-values into lists
for k, v in databank:
    if databank['Country']:
        value = databank['Country']
        k:list(map(value.split(', ')))

#  remove charity duplicates 
for i in databank:
    if DATABANK.has_key('charity name'):
        pass 
    else:
        DATABANK.append(i)

print(len(DATABANK))

# if databank['Categories'] == DATABANK['Categories']:
#     for i in databank['Country']:
#        if not in DATABANK['Country']:
#            DATABANK['Country'].append(i)
#        else:
#            pass   
