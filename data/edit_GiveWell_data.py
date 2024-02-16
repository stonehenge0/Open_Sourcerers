import os
import pandas as pd
import re


# Get the relative file name for the ordered_CONSTANTS file, provided script and datafile are stored in the same folder.
script_dir = os.path.dirname(__file__)
data_filename = "\\ordered_CONSTANTS.xlsx"
data_path = script_dir+data_filename

# Turn excel file into panda dataframe.
df = pd.read_excel(data_path)


# Turning the string in the cost-efficiency column to lists
def string_to_list(string):
    if string == "[]":
        return []
    
    else:
        ls = string.strip('][').replace("'","").split(', ')
        return ls

df['Cost-efficiency'] = df['Cost-efficiency'].apply(lambda x: string_to_list(x))



## Extracting only the relevant Google Doc links from all the ones I have in ordered_constants. 

def extract_spreadsheet_id(google_sheets_link):
    """Extracts the unique identifier of a google sheet link using regEx
    ---
    input: A google sheet link
    output: the spreadsheet id. If there isn't one, it returns None."""
    # Define a regular expression pattern that matches spreadsheet ID.
    pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'

    # Use re.search to find the match in the link.
    match = re.search(pattern, google_sheets_link)

    # Check if a match is found.
    if match:
        spreadsheet_id = match.group(1)
        return spreadsheet_id
    else:
        # If no match is found, return None.
        return None


def get_final_ce_link(links):
    """Gets rid of all doubled links that have the same id, searches for Cost-effectiveness in that sheet and returns one final link.
    
    
    input: a list of strings that represent the links to Google Sheet documents. If the list is empty, function returns an empty list.
    output: A single link to a Google sheet document that is unique and mentions cost-effectiveness."""
    
    if not links: # Check if the input list is empty.
        return []
    
    else:
        # Get unique link ids.  
        id_set = list(set([extract_spreadsheet_id(link) for link in links] )) # And then turn back into list to work with better afterwards.
      
      
        # Turning the ids back into full google doc links. 
        unique_links = ["https://docs.google.com/spreadsheets/d/"+id for id in id_set if id]  
        
        
        # List will contain all unique links that mention cost-effectiveness. 
        finished_links = []
        
        # Define search term.
        search_term = "cost-effectiveness"

        # Check whether a google sheet contains "cost-effectiveness"
        for link in unique_links:
            
            try: 
                df = pd.read_csv(link, on_bad_lines='skip', low_memory=False) # The skip is in here, because otherwise it can't read the df in properly.
            except:
                print("Some error occured!")
            
            # Use applymap and str.contains to check for the presence of the the string "cost-effectiveness".
            found_term = df.applymap(lambda cell: search_term.lower() in str(cell).lower()).any().any() # The .any is there to get it from a pandas df object into a boolean. 

            # Append to final out list if found. 
            if found_term:
                finished_links.append(link)
              
        final_link = finished_links[:1]     # return only one link in the end. 
        
        return final_link



# Apply the function to the cost-effectiveness column and hope nothing breaks. 
df['final_ce'] = df['Cost-efficiency'].apply(lambda link_list: get_final_ce_link(link_list))

# Write the modified DataFrame to an Excel file named 'finished_ce.xlsx'
output_excel_file = 'finished_ce.xlsx'
df.to_excel(output_excel_file, index=False)


