""" Map GiveWell grants to continents and scrape cost-effectiveness sheets.


NOTE: The dependency pycountry_convert needs to be installed separately.
NOTE: When you run this program, it will most likely return an error message like this one: 
 "UserWarning: Country's common_name not found. Country name provided instead.". You can ignore 
 the errormessage, it just means that a different way of naming a Country had to be provided (that
 is still recognizable and ISO coded), so it will not cause problems down the line. 

"""

import os

import requests
import pandas as pd
from bs4 import BeautifulSoup 
import pycountry_convert as pc 


def transform_to_list(value):
    """Transform the entries in a cell to a list, split by commata. 
    Intended to split dataframe entries by comma to become different list entries. 

    Args:
        cell (str): An entry of a cell in a pandas dataframe.

    Returns:
        list: list of values, split by commata. Returns an empty list if the cell is empty. 
    """
    
    if pd.isna(value):  
        return []  # Return an empty list for empty cells
    else:
        return [part.strip() for part in value.split(',')]
    
    
def country_to_continent(country_name):
    """Convert a country name to a continent name using their ISO numbers.

    Args:
        country_name (str): country

    Returns:
        str: continent
    """
    
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    
    return country_continent_name


def scrape_unique_google_doc_links(url):
    """ Get unique links to Google Docs in a given url.

    Args:
        url (str): a url in full form (http/:...)

    Returns:
        list: unique Google Document links
    """

    # Send a GET request to the URL.
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=True)
            
        unique_google_doc_links = []

        for link in links:
            if 'docs.google.com' in link['href'] and link["href"] not in unique_google_doc_links:
                unique_google_doc_links.append(link['href'])


        return unique_google_doc_links

    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")

    




## Read in data.
script_dir = os.path.dirname(__file__)
data_filename = "\\GiveWell_grant_data_original.xlsx"
data_path = script_dir+data_filename

df_grant = pd.read_excel(data_path)


# Columns are not needed for our purposes, so they get dropped. 
columns_to_drop = ["Grant Name","date","Grant Amount", "Grant Type"]
df_grant = df_grant.drop(columns_to_drop, axis='columns')

df_grant.drop_duplicates(subset='Charity Name', keep='first', inplace=True)




## Map Countries to Continents.
df_grant['Country'] = df_grant['Country'].apply(transform_to_list)

# Create a new "Continent" column. 
df_grant.insert(4,"Continent", "")

df_grant['Continent'] = df_grant['Country'].apply(lambda countries_list: [country_to_continent(country) for country in countries_list] if countries_list else [])




## Webscrape Links to the cost-effectiveness sheets and writing to the "Cost-efficiency" cloumn.
df_grant.insert(5,"Cost-efficiency", "")

df_grant['Cost-efficiency'] = df_grant['Grant Website'].apply(scrape_unique_google_doc_links)




## Add columns required to fit well in the database. 
df_grant.insert(6,"Evaluator", "GiveWell")
df_grant.insert(7,"X-Crisis", "n")
df_grant.insert(8,"Efficiency Rating", "4") # This will be modified later on. This is just to set a value there.

# Order the df. 
df_grant = df_grant.loc[
    :,
    [
        "Charity Name",
        "Categories",
        "X-Crisis",
        "Country",
        "Continent",
        "Efficiency Rating",
        "Evaluator",
        "Grant Website",
        "Cost-efficiency",
    ],
]


df_grant.to_excel("GiveWell_extracted_webscraped.xlsx")

# Optional: inspect the head of the dataframe. 
# print(df_grant.head())


