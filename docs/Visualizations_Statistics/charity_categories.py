## This plot visualizes the charity categories and how many charities we have in each section with a circular boxplot. 
# Most of the code is adapted from Python Graph Gallery: https://python-graph-gallery.com/circular-barplot/ 

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict


def split_values (Instring):
    """takes a string and makes it into a list of coma seperated values that are stripped from whitespace.

    Args:
        Instring (string): A string containing multiple values we want to split.

    Returns:
        List: a list of strings 
    """
    split_values = Instring.split(",") 
    striped_values = [item.strip() for item in split_values]
    return (striped_values)

def clean_string(input_string): #This will be used for the DZI data since it has "\" these in it a lot. 
    """
    Cleans a string by removing all non-alphanumeric characters, except commas.

    Parameters:
    - input_string (str): The input string to be cleaned.

    Returns:
    - str: The cleaned string.
    """
    cleaned_string = ''.join(char if char.isalnum() or char == ',' else ' ' for char in input_string)
    return cleaned_string
    

# Reading in datasets. (Change that this is hardcoded?)
ACE_data_filename = "C:\\Users\\emste\\Documents\\GitHub\\Open_Sourcerers\\data\\final_ACE.xlsx"
DZI_data_filename = "C:\\Users\\emste\\Documents\\GitHub\\Open_Sourcerers\\data\\final_DZI.xlsx"
GW_data_filename = "C:\\Users\\emste\\Documents\\GitHub\\Open_Sourcerers\\data\\final_GiveWell_and_GWWC.xlsx"


# Turning sheets into dataframes.
ACE_df = pd.read_excel(ACE_data_filename)
DZI_df = pd.read_excel(DZI_data_filename)
GW_df = pd.read_excel(GW_data_filename)

# Getting the category column of each df into a list. 
ACE_list = ACE_df["category"].tolist()
DZI_list = DZI_df["category"].tolist()
GW_list = GW_df["Categories"].tolist()

# The DZI list has "\" and a bunch of other stuff in it we want to get rid of. 
DZI_list = [clean_string(item) for item in DZI_list]

# Get all lists into same format, namely a list of lists containing strings.
ACE_list = [split_values(item) for item in ACE_list]
GW_list = [split_values(item) for item in GW_list]
DZI_list = [split_values(item) for item in DZI_list]

# Flatten individual lists. 
ACE = [item for sublist in ACE_list for item in sublist]
DZI = [item for sublist in DZI_list for item in sublist]
GW = [item for sublist in GW_list for item in sublist]

# Put all three lists together into one big one. 
all_values = ACE + DZI + GW



# Initialize an empty defaultdict to store the counts
counter_dict = defaultdict(int)

# Count the occurrences of each string
for item in all_values:
    counter_dict[item] += 1

# Convert defaultdict to a regular dictionary if needed
final_dict = dict(counter_dict)

# Change a label name, because it was so long it wasn't being displayed correctly 
final_dict["campaigning and education"] = final_dict.pop("campaigning and educational work")









# Set figure size
plt.figure(figsize=(20, 10))

# Plot polar axis
ax = plt.subplot(111, polar=True)

# Remove grid
plt.axis('off')

# Set the coordinates limits
upperLimit = 100
lowerLimit = 30

# Compute max and min in the dataset
max_value = max(final_dict.values())

# Computing heights: heights are a conversion of each item value in those new coordinates.
slope = (max_value - lowerLimit) / max_value
heights = [slope * value + lowerLimit for value in final_dict.values()]

# Compute the width of each bar. In total we have 2*Pi = 360°
width = 2 * np.pi / len(final_dict)

# Compute the angle each bar is centered on:
indexes = list(range(1, len(final_dict) + 1))
angles = [element * width for element in indexes]

# Initialize the figure
plt.figure(figsize=(20, 10))
ax = plt.subplot(111, polar=True)
plt.axis('off')

# Draw bars
bars = ax.bar(
    x=angles,
    height=heights,
    width=width,
    bottom=lowerLimit,
    linewidth=2,
    edgecolor="white",
    color="#61a4b2",
)

# Little space between the bar and the label
labelPadding = 4

# Add labels.
for bar, angle, height, (label, value) in zip(bars, angles, heights, final_dict.items()):
    # Labels are rotated. Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle)

    # Flip some labels upside down for visibility.
    alignment = ""
    if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
        alignment = "right"
        rotation = rotation + 180
    else:
        alignment = "left"

    # Add labels finally.
    ax.text(
        x=angle,
        y=lowerLimit + bar.get_height() + labelPadding,
        s=f'{label}: {value}',
        ha=alignment,
        va='center',
        rotation=rotation,
        rotation_mode="anchor"
    )

plt.show()
