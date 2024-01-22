
import os
import pandas as pd
import pycountry # Used to map countries to continents.
import pycountry_convert as pc # Importantly, this needs an extra $ pip install pycountry-convert to work.
import requests
from bs4 import BeautifulSoup 
import hashlib # Used to check whether different webscraped Google Doc Links might lead to the same document. 


# Get the relative file name for the grant_data file, provided script and datafile are stored in the same folder.
script_dir = os.path.dirname(__file__)
data_filename = "\\grant_data.xlsx"
data_path = script_dir+data_filename

# Turn excel file into panda dataframe.
df_grant = pd.read_excel(data_path)

# Removing columns that are not needed for our purposes.
columns_to_drop = ["Grant Name","date","Grant Amount", "Grant Type"]
df_grant = df_grant.drop(columns_to_drop, axis='columns')

# Removing duplicates (No charity should appear twice in the final list).
df_grant.drop_duplicates(subset='Charity Name', keep='first', inplace=True)


## Mapping Countries to Continents.
# Turning the entries in the "country" section into lists, so we can work with them better afterwards. 
def transform_to_list(value):
    """This function makes the entries in a cell into a list. If entry is empty, returns an empty list. Splits entries by comma to become different list entries."""
    
    if pd.isna(value):  # Check if the value is NaN (empty cell).
        return []  # Return an empty list for empty cells
    else:
        # Split the string by commas and strip whitespace from each part
        return [part.strip() for part in value.split(',')]

# Apply the transformation function to the country column.
df_grant['Country'] = df_grant['Country'].apply(transform_to_list)

# Create a new "Continent" column. 
df_grant.insert(4,"Continent", "")

# Function maps a country to its continent using the pycountry library.
def country_to_continent(country_name):
    """input: country name. 
    output: continent name. 
    This function converts a country name to a continent name by converting to their ISO numbers and back."""
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

# Fill in the Continent cells based on the Country they are active in.
df_grant['Continent'] = df_grant['Country'].apply(lambda countries_list: [country_to_continent(country) for country in countries_list] if countries_list else [])





## Webscraping Links to the cost-effectiveness sheets.
# List of all GiveWell program review Urls. 
GiveWell_urls = df_grant['Grant Website'].tolist()

# Create a new "Cost-efficiency" column. 
df_grant.insert(5,"Cost-efficiency", "")

# Function to scrape unique links to Google Docs from a given URL
def scrape_unique_google_doc_links(url):
    """input: url
    output: list of unique Google Doc links in given url"""
    try:
        # Send a GET request to the URL.
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Create a Beautiful Soup object
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get all href tags
            links = soup.find_all('a', href=True)

            # Make sure that links are unique. 
            unique_google_doc_links = set()

            # Iterate over links and add unique Google Doc links to the set.
            for link in links:
                if 'docs.google.com' in link['href']:
                    unique_google_doc_links.add(link['href'])

            # Convert set to list.
            unique_google_doc_links_list = list(unique_google_doc_links)

            #return the unique Google Doc links list.
            return unique_google_doc_links_list

        else: 
            print(f"Failed to retrieve the page. Status Code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Applying the google_doc_scrape function to each link in the document and getting the cost-effectiveness links. 
df_grant['Cost-efficiency'] = df_grant['Grant Website'].apply(scrape_unique_google_doc_links)

# Kicking Google Doc links that actually lead to the same document using hashes. 
# ...





# Turn the final df into an excel table. 
df_grant.to_excel("CONSTANTS.xlsx")

