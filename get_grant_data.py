import os
import pandas as pd

#   get the relative file name for the grant_data file, provided script and datafile are stored in the same folder
script_dir = os.path.dirname(__file__)
data_filename = "\\grant_data.xlsx"
data_path = script_dir+data_filename
print(data_path)

#   get the relative file name for the databank file, provided script and databankfile are stored in the same folder
databank_filename = "\\databank.py"
databank_path = script_dir+databank_filename
print(databank_path)

#   turn datafile into panda dataframe
df_grant = pd.read_excel(data_path)

# nested dict with charity names a child-dicts
databank = {}

# get relevant data columns and remove duplicates
for label = 'Charity Name' in df_grant:
    if i is not in databank:
        # create entry in databank with charity name as dictionary name, categories and country as keys with values as list

        



