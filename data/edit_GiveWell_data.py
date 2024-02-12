
import os
import pandas as pd
import requests
import hashlib # Used to check whether different webscraped Google Doc Links might lead to the same document. 
from urllib.parse import urlsplit, parse_qs


# Get the relative file name for the ordered_CONSTANTS file, provided script and datafile are stored in the same folder.
script_dir = os.path.dirname(__file__)
data_filename = "\\ordered_CONSTANTS.xlsx"
data_path = script_dir+data_filename

# Turn excel file into panda dataframe.
df = pd.read_excel(data_path)


# Function gets the document ID from Google Sheets link.
def extract_doc_id(link):
    """Extracts the Document id from a given Google Doc link. Only works with Google doc, not with other forms of links etc.
    input: link to a Google Doc
    Output: The id for that Document """
    return parse_qs(urlsplit(link).query)['id'][0]

# Apply the function to create a new column with document IDs
df['Doc_ID'] = df['Cost-efficiency'].apply(lambda x: [extract_doc_id(link) for link in x])

# Remove duplicate document IDs
df['Unique_Doc_ID'] = df['Doc_ID'].apply(lambda x: list(set(x)))

# Remove intermediate columns if not needed
# df = df[['Cost-efficiency', 'Unique_Doc_ID']]

print(df[["Cost-efficiency", "Unique_Doc_ID"]])


print("Hello!")


