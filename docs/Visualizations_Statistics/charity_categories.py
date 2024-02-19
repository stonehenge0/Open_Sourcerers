""" Plots a circular barplot of what categories our charities fall in and how many are in each category.. 
"""

# Code for the plot adapted from: https://python-graph-gallery.com/circular-barplot/


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict
import os
from collections import defaultdict

def split_values (Instring):
    """Turn a string into a list of comma seperated values stripped from whitespace.

    Args:
        Instring (string): A string containing the  values we want to split.

    Returns:
        List: a list of strings 
    """
    split_values = Instring.split(",") 
    striped_values = [item.strip() for item in split_values]
    return (striped_values)

def clean_string(input_string): 
    """
    Remove all non-alphanumeric characters, except commas.

    Parameters:
    - input_string (str): The input string to be cleaned.

    Returns:
    - str: The cleaned string.
    """
    cleaned_string = ''.join(char if char.isalnum() or char == ',' else ' ' for char in input_string)
    return cleaned_string
    

## Read in data.
base_dir = os.path.dirname(__file__) 

grandparent_dir = os.path.dirname(os.path.dirname(base_dir)) # Move up two levels to acces the data folder.

data_folder = os.path.join(grandparent_dir, 'data')

ACE_data_filename = os.path.join(data_folder, 'final_ACE.xlsx')
DZI_data_filename = os.path.join(data_folder, 'final_DZI.xlsx')
GW_data_filename = os.path.join(data_folder, 'final_GiveWell_and_GWWC.xlsx')

ACE_df = pd.read_excel(ACE_data_filename)
DZI_df = pd.read_excel(DZI_data_filename)
GW_df = pd.read_excel(GW_data_filename)

ACE_list = ACE_df["category"].tolist()
DZI_list = DZI_df["category"].tolist()
GW_list = GW_df["Categories"].tolist()


## Clean and formalise data.
# The DZI list has "\" and a bunch of other stuff in it we want to get rid of. 
DZI_list = [clean_string(item) for item in DZI_list]

ACE_list = [split_values(item) for item in ACE_list]
GW_list = [split_values(item) for item in GW_list]
DZI_list = [split_values(item) for item in DZI_list]

# Flatten lists. 
ACE = [item for sublist in ACE_list for item in sublist]
DZI = [item for sublist in DZI_list for item in sublist]
GW = [item for sublist in GW_list for item in sublist]

all_values = ACE + DZI + GW


## Count occurrences of categories.
counter_dict = defaultdict(int)

for item in all_values:
    counter_dict[item] += 1

final_dict = dict(counter_dict)

# Kick low values and shorten some label names for better visibility.
final_dict["campaigning and education"] = final_dict.pop("campaigning and educational work")
final_dict["healthcare"] = final_dict.pop("healthcare and prevention")
final_dict = {key:val for key, val in final_dict.items() if val >= 5}






# I left most of the comments from the original post, as I found it quite helpful to understand
# the making of the circular barplot a bit more in-depth. 


# Set figure size.
plt.figure(figsize=(20, 10)) 

# Plot polar axis.
ax = plt.subplot(111, polar=True)

# Remove grid.
plt.axis('off')

# Set the coordinates limits.
upperLimit = 100
lowerLimit = 30

# Compute max and min in the dataset.
max_value = max(final_dict.values())

# Computing heights: heights are a conversion of each item value in those new coordinates.
slope = (max_value - lowerLimit) / max_value
heights = [slope * value + lowerLimit for value in final_dict.values()]

# Compute the width of each bar. In total we have 2*Pi = 360°.
width = 2 * np.pi / len(final_dict)

# Compute the angle each bar is centered on:
indexes = list(range(1, len(final_dict) + 1))
angles = [element * width for element in indexes]

# Initialize the figure.
plt.figure(figsize=(20, 10))
ax = plt.subplot(111, polar=True)
plt.axis('off')

# Draw bars.
bars = ax.bar(
    x=angles,
    height=heights,
    width=width,
    bottom=lowerLimit,
    linewidth=2,
    edgecolor="white",
    color="#61a4b2",
)

# Little space between the bar and the label.
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
