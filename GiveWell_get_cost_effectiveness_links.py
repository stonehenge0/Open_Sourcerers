"""Extract one final link to Cost-effectiveness analysis from a list of different possible
    links from the webscraping. 
    

    Returns:
        .xlsx file: Excel file, where the cost-effectiveness column has one final value.  
 """

import os

import re
import pandas as pd

def extract_spreadsheet_id(google_sheets_link):
    """Extract unique identifier (id) of a google sheet link using RegEx.
    
    Please not that this ONLY works for google sheet links, not for links in a different format. 

    Args:
        google_sheets_link (str): A link to a google sheet document.

    Returns:
        str: id. If no matches are found, returns None
    """
    # This pattern matches the spreadsheet ID specifically of a Google Docs. 
    pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)' 

    match = re.search(pattern, google_sheets_link)

    if match:
        spreadsheet_id = match.group(1)
        return spreadsheet_id
    else:
        return None 


def get_final_ce_link(links):
    """Remove links with same id, or that do not mention "cost-effectiveness" and returns one link.

    Args:
        links (list): List of Google Doc links.

    Returns:
        str: a single link that is unique and mentions cost-effectiveness.
    """    

    if not links:
        return []
    
    else:
        # Get unique link ids.  
        id_set = list(set([extract_spreadsheet_id(link) for link in links] )) # And then turn back into list to work with better afterwards.
      
      
        # Turn ids back into full google doc links. 
        unique_links = ["https://docs.google.com/spreadsheets/d/"+id for id in id_set if id]  
        
        finished_links = []
        
        search_term = "cost-effectiveness"

        # Check whether a google sheet contains "cost-effectiveness"
        for link in unique_links:
            
            try: 
                df = pd.read_csv(link, on_bad_lines='skip', low_memory=False) # The skip is necessary here, because otherwise it can't read the df in properly.
                
            except Exception as e:
                print(f"Error occurred while reading CSV from {link}: {e}")
                print("Please ensure that the file exists and is in a valid CSV format.")
                continue
            
            # Check for the presence of the the string "cost-effectiveness".
            found_term = df.applymap(lambda cell: search_term.lower() in str(cell).lower()).any().any() # The .any part is there to get it from a pandas df object into a boolean. 

            if found_term:
                finished_links.append(link)
              
        final_link = finished_links[:1]    # return only one link in the end. 
        
        return final_link



## Read in files.
script_dir = os.path.dirname(__file__)
data_filename = "\\ordered_CONSTANTS.xlsx"
data_path = script_dir+data_filename

df = pd.read_excel(data_path)


if __name__ == "__main__":
    df['final_ce'] = df['Cost-efficiency'].apply(lambda link_list: get_final_ce_link(link_list))

    output_excel_file = 'finished_ce.xlsx'
    df.to_excel(output_excel_file, index=False)


