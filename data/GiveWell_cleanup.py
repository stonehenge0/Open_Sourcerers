"""Small adjustments to GW data: Remove accidental duplicates in columns, and map their
    cost-effectiveness ratings to ours. 
    
    returns:
        the final data from GiveWell. 
"""

import os

import pandas as pd


# Get the relative file name for the file, provided script and datafile are stored in the same folder.
script_dir = os.path.dirname(__file__)
data_filename = "\\GiveWell_almost_finished.xlsx"
data_path = script_dir+data_filename

df = pd.read_excel(data_path)

# Remove unwanted columns. The cost efficiency stays in there, I just accidentally made two of it, and had to remove one.
df = df.drop(columns =['Unnamed: 0', 'Cost-efficiency'])
df = df.rename(columns={'final_ce': 'Cost-efficiency'})


# Adapt efficiency scores to fit our general guidelines for all charities.
df.loc[df["Efficiency Rating"] == 4, "Efficiency Rating"] = 3
df.loc[df["Efficiency Rating"] == 5, "Efficiency Rating"] = 4


df.to_excel("final_GiveWell_and_GWWC.xlsx")