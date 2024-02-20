# -*- coding: utf-8 -*-
"""Doing Search.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uFqGZaj25w4ekeMROc_xA4jfrI8ZAD3d
"""

##read the dataset
import numpy as np
import pandas as pd
import ast
import os
from io import BytesIO
import base64
import matplotlib.pyplot as plt
def main(user_continent, user_country, user_category
         , user_x, user_eff
         , directory_of_dataset = os.path.join(os.getcwd(),"data", "final_cleaned_meaningful_all.csv")):
  import numpy as np
  import pandas as pd
  import ast
  import os
  from io import BytesIO
  import base64
  import matplotlib.pyplot as plt
  country_levels = pd.read_csv(os.path.join(os.getcwd(),"data","country_levels.csv"))
  category_levels = pd.read_csv(os.path.join(os.getcwd(),"data","category_levels.csv"))
  continent_levels = pd.read_csv(os.path.join(os.getcwd(),"data","continent_levels.csv"))
  temp = []
  for i in user_continent:
    temp.append(int(i))
  user_continent = temp
  temp = []
  for i in user_category:
    try:
      temp.append(int(i))
    except Exception:
      continue
  user_category = temp
  temp = []
  for i in user_country:
    try:
      temp.append(int(i))
    except Exception:
      continue
  user_country = temp

  if user_x == 'no':
    user_x = [0]
  else:
    user_x = [1]

  user_eff = [int(user_eff)]
  f = pd.read_csv(directory_of_dataset)
  ##create a function as distance metric to calculate similarity between what user entered and the charities existed in the dataset
  ##first, it gives the exact mathces between user entry and dataset 5 score, then it searched over similar category feature and gave a score depeneds on similarity between user input and dataset
  def iterate_1(amount, vec):
    dists = [((amount-x)**2)**0.5 for x in vec if ((amount-x)**2)**0.5 <= 3]
    try:
      return(min(dists))
    except Exception:
      return(0)
  def calculate_over_all(column, wanted, feature = False):
    scores = []
    k = 0
    try:
      desired_vector = ast.literal_eval(column)
    except Exception:
      desired_vector = column

    for i in wanted:
      if i in desired_vector:
        k = k + 10
      elif i not in desired_vector and feature:
        k = k + iterate_1(i,desired_vector)
    return(k)
  ##iterate over all dataset to find similar matches to user entry
  total_scores = []
  for index, row in f.iterrows():
    v_1 = calculate_over_all(row['categ_continent'], user_continent)
    print(user_eff)
    print(row['efficiency'])
    v_2 = calculate_over_all([row['efficiency']], user_eff)
  #print(row['country'])
    v_3 = calculate_over_all(row['categ_country'], user_country)
    v_4 = calculate_over_all(row['categ_category'], user_category, True)
  #print(row['categ_x'])
    v_5 = calculate_over_all([row['categ_x']], user_x, 1)
    total_scores.append((0.5 * v_1+ 0.8 * v_2+0.5 * v_3+0.6 * v_4+0.9 * v_5))
  ##sort the results based on their similarity score
  emp_dic = {}
  k = 0
  for i in total_scores:
    emp_dic[k] = i
    k = k + 1
  sorted_dic = dict(sorted(emp_dic.items(), key=lambda x:x[1] , reverse= True))
  ##define filtering function
  def filter_rows(column, criteria):
    index = []
    for i in column:
      try:
        vector = ast.literal_eval(i)
      except Exception:
        vector = [i]
      flag = 0
      for j in criteria:
        if j in vector:
          index.append(True)
          flag = 1
          break
      if flag == 1:
        continue
      else:
        index.append(False)
    return(index)
  ##do exact match
  g = f.loc[filter_rows(f['categ_continent'], user_continent), :]
  g = g.loc[filter_rows(g['categ_country'], user_country), :]
  g = g.loc[filter_rows(g['categ_category'], user_category), :]
  g = g.loc[filter_rows(g['efficiency'], user_eff), :]
  g = g.loc[filter_rows(g['categ_x'], user_x), :]
  ##do similarit check to rank the exact search results
  total_scores_1 = []
  for index, row in g.iterrows():
    v_1 = calculate_over_all(row['categ_continent'], user_continent)
  #print(row['efficiency'])
    v_2 = calculate_over_all([row['efficiency']], user_eff)
  #print(row['country'])
    v_3 = calculate_over_all(row['categ_country'], user_country)
    v_4 = calculate_over_all(row['categ_category'], user_category, True)
  #print(row['categ_x'])
    v_5 = calculate_over_all([row['categ_x']], user_x)
    total_scores_1.append((0.5 * v_1+ 0.8 * v_2+0.5 * v_3+0.6 * v_4+0.9 * v_5))
  emp_dic_1 = {}
  k = 0
  for i in total_scores_1:
    emp_dic_1[k] = i
    k = k + 1
  sorted_dic_1 = dict(sorted(emp_dic_1.items(), key=lambda x:x[1] , reverse= True))
  flag = 0
  if len(sorted_dic_1) >= 3:
    names = [g.iloc[int(x),1] for x in list(sorted_dic_1.keys())[0:3]]
    counts = list(sorted_dic_1.values())[0:3]
    ins1 = f.iloc[list(sorted_dic_1.keys())[0],:].to_dict()
    ins2 = f.iloc[list(sorted_dic_1.keys())[1],:].to_dict()
    ins3 = f.iloc[list(sorted_dic_1.keys())[2],:].to_dict()
    if 'global' in ast.literal_eval(ins1['country']):
      ins1['continent'] = 'all'  
    if 'global' in ast.literal_eval(ins2['country']):
      ins2['continent'] = 'all'    
    if 'global' in ast.literal_eval(ins3['country']):
      ins3['continent'] = 'all'      

    if len(ast.literal_eval(ins1['country'])) == 0:
      ins1['country'] = 'almost all countries'
    if len(ast.literal_eval(ins2['country'])) == 0:
      ins2['country'] = 'almost all countries'
    if len(ast.literal_eval(ins3['country'])) == 0:
      ins3['country'] = 'almost all countries'
    results = {'result1' : ins1, 'result2' : ins2, 'result3' : ins3}
    flag = 1
  else:
    names = [f.iloc[int(x),1] for x in list(sorted_dic.keys())[0:3]]
    counts = list(sorted_dic.values())[0:3]
    ins1 = f.iloc[list(sorted_dic.keys())[0],:].to_dict()
    ins2 = f.iloc[list(sorted_dic.keys())[1],:].to_dict()
    ins3 = f.iloc[list(sorted_dic.keys())[2],:].to_dict()
    if 'global' in ast.literal_eval(ins1['country']):
      ins1['continent'] = 'all'  
    if 'global' in ast.literal_eval(ins2['country']):
      ins2['continent'] = 'all'    
    if 'global' in ast.literal_eval(ins3['country']):
      ins3['continent'] = 'all'      
    if len(ast.literal_eval(ins1['country'])) == 0:
      ins1['country'] = 'almost all countries'
    if len(ast.literal_eval(ins2['country'])) == 0:
      ins2['country'] = 'almost all countries'
    if len(ast.literal_eval(ins3['country'])) == 0:
      ins3['country'] = 'almost all countries'
    results = {'result1' : ins1, 'result2' : ins2, 'result3' : ins3}
    flag = 1
  ##plot the 3 topmost results
  if flag == 1:
    fig, ax = plt.subplots()
    img = BytesIO()
    ax.pie(counts, labels=names, autopct='%1.1f%%')
    plt.savefig(img, format='JPEG')
    plt.close()
    #img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    #plt.savefig("/result1.png", pad_inches = 0.2, bbox_inches = 'tight')
  return(results,plot_url)







