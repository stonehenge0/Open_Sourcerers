
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup 
import hashlib # Used to check whether different webscraped Google Doc Links might lead to the same document. 

# Get the relative file name for the ordered_CONSTANTS file, provided script and datafile are stored in the same folder.
script_dir = os.path.dirname(__file__)
data_filename = "\\ordered_CONSTANTS.xlsx"
data_path = script_dir+data_filename

# Turn excel file into panda dataframe.
df = pd.read_excel(data_path)




