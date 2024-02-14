import os
import pandas as pd
# Look at a way to make this more efficient thatn just creating a lot of copies. 


# Get the relative file name for the file, provided script and datafile are stored in the same folder.
script_dir = os.path.dirname(__file__)
data_filename = "\\semi_finished_GIveWell.xlsx"
data_path = script_dir+data_filename

# Turn excel file into panda dataframe.
df = pd.read_excel(data_path)

# Removing unwanted columns. (the cost efficiency is still in there, I just accidentally made two of it.)
df = df.drop(columns =['Unnamed: 0', 'Cost-efficiency'])

# Rename the right column. 
df = df.rename(columns={'final_ce': 'Cost-efficiency'})

# Make values in Efficiency from strings to integers. 
# Adapt efficiency scores to fit our general guidelines for all charities.
df.loc[df["Efficiency Rating"] == 4, "Efficiency Rating"] = 3
df.loc[df["Efficiency Rating"] == 5, "Efficiency Rating"] = 4


# Write the DataFrame to an Excel file
df.to_excel("final_GiveWell_and_GWWC.xlsx")











