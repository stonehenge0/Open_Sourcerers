
import os
import pandas as pd
import pycountry # Used to map countries to continents later on.
import pycountry_convert as pc # Importantly, this needs an extra $ pip install pycountry-convert to work, since it is NOT in the initial pycountry module install


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

# Fill in the Continent cells with the continent that charity is active in, based on the countries they are active in. 
#...




