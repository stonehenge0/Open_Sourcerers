# -*- coding: utf-8 -*-
"""data_cleaning_perform on whole dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11-wyIPtntZ7uIxGxK7pebteiCMUOARd2
"""

##read the whole dataset
import numpy as np
import pandas as pd
d = pd.read_excel("/content/cleaned_full_data.xlsx")

##find unique continents used in dataset
##the lists in the dataset were saved in string format, so, we use ast package to reconvert the string to list
uniques_cont = []
for index, i in enumerate(d['continent']):
  try:
    continents = ast.literal_eval(i)
    [uniques_cont.append(x) for x in continents if x not in uniques_cont]
    d['continent'][index] = continents
  except Exception:
    d['continent'][index] = []

##find unique countries used in dataset
uniques_country = []
for index, i in enumerate(d['country']):
  try:
    countries = ast.literal_eval(i)
    [uniques_country.append(x) for x in countries if x not in uniques_country]
    d['country'][index] = countries
  except Exception:
    d['country'][index] = []

##categorize_continents
##the categ_cont is categorized format of continent feature
categ_cont = []
for i in d['continent']:
  if 'Africa' in i:
    categ_cont.append([2])
  elif 'Asia' in i:
    categ_cont.append([1])
  elif 'Europe' in i:
    categ_cont.append([3])
  elif 'North America' in i:
    categ_cont.append([4])
  elif 'South America' in i:
    categ_cont.append([5])
  elif 'global' in i:
    categ_cont.append([1,2,3,4,5])

##help to find geographical features of countries
!pip install geopy
from geopy.geocoders import Nominatim

# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")

location = geolocator.geocode("Hyderabad")

##categorize_country
##first, sort the list of countries using distance between a reference country (Japan) and other countries
##then, assign a level to each country considering assigning level 1 to reference country and the level increased based on distance metric
##country_categ is a dictionary with keys represent countries and values representing levels assigned in previous step.
from geopy.geocoders import Nominatim
import geopy.distance
geolocator = Nominatim(user_agent="MyApp")
reference = geolocator.geocode("Japan").point[0:2]
count_dist = {}
for i in uniques_country:
  second = geolocator.geocode(i).point[0:2]
  distance = geopy.distance.geodesic(reference, second).km
  count_dist[i] = distance
sorted_distance = dict(sorted(count_dist.items(), key=lambda x:x[1]))
country_categ = {}
level = 1
for i in sorted_distance.keys():
  country_categ[i] = level
  level += 1

##applying country categorization on dataset
##categ_country is a categorized format of country feature in dataset
categ_country = []
for i in d['country']:
  try:
    categs = [country_categ[x] for x in i]
    if len(categs) == 0:
      categ_country.append([i for i in range(1,182)])
    else:
      categ_country.append(categs)
  except Exception:
    categ_country.append([i for i in range(1,182)])

##categorise category
##find unique categories written in the dataset
uniques_categories = []
for index, i in enumerate(d['category']):
  try:
    categories = ast.literal_eval(i)
    [uniques_categories.append(x) for x in categories if x not in uniques_categories]
    d['category'][index] = categories
  except Exception:
    splits = i.split(",")
    categories = [x.strip() for x in splits]
    d['category'][index] = categories
    [uniques_categories.append(x) for x in categories if x not in uniques_categories]

##create a category_levels dictionary which assigns a level to each category
category_levels = {}
levels = 1
for i in uniques_categories:
  category_levels[i] = levels
  levels += 1

##import new categorization method to count relation between different categories
new_category_levels = pd.read_csv("/content/category_levels.csv")
category_levels = {}
for index, i in enumerate(new_category_levels['category']):
  category_levels[i] = int(new_category_levels['meaningful_levels'][index])

##applying category categorisation on dataset
categ_category = []
for i in d['category']:
  categ_category.append([category_levels[x] for x in i])

##insert the created categorized version of features into original dataset
d.insert(loc= d.shape[1], column='categ_continent', value=categ_cont, allow_duplicates=True)
d.insert(loc= d.shape[1], column='categ_country', value=categ_country, allow_duplicates=True)
d.insert(loc= d.shape[1], column='categ_category', value=categ_category, allow_duplicates=True)

##save the modified dataset
d.to_csv("/content/final_cleaned_all.csv")

##save different features with their assigned levels
data_country = {'country' : country_categ.keys(), 'levels' : country_categ.values()}
c_1 = pd.DataFrame(data_country)
data_category = {'category' : category_levels.keys(), 'levels' : category_levels.values()}
c_2 = pd.DataFrame(data_category)
c_1.to_csv("/content/country_levels.csv")
c_2.to_csv("/content/category_levels.csv")