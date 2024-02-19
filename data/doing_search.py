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
def main(user_continent = [1,2,3,4,5], user_country = [81,90,105], user_category = [52, 42]
         , user_x = [0], user_eff = [3]
         , directory_of_dataset = "/final_cleaned_meaningful_all.csv"):
    f = pd.read_csv(directory_of_dataset) ##read the dataset

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
          k = k + 5
        elif i not in desired_vector and feature:
          k = k + iterate_1(i,desired_vector)
      return(k)

##iterate over all dataset to find similar matches to user entry
    total_scores = []
    for index, row in f.iterrows():
      v_1 = calculate_over_all(row['categ_continent'], user_continent)
  #print(row['efficiency'])
      v_2 = calculate_over_all([row['efficiency']], user_eff)
  #print(row['country'])
      v_3 = calculate_over_all(row['categ_country'], user_country)
      v_4 = calculate_over_all(row['categ_category'], user_category, True)
  #print(row['categ_x'])
      v_5 = calculate_over_all([row['categ_x']], user_x, 1)
      total_scores.append((0.1 * v_1+ 0.1 * v_2+0.1 * v_3+0.9*v_4+0.1* v_5))

##sort the results based on their similarity score
    emp_dic = {}
    k = 0
    for i in total_scores:
      emp_dic[k] = i
      k = k + 1
    sorted_dic = dict(sorted(emp_dic.items(), key=lambda x:x[1] , reverse= True))

"""Exact Search"""

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
    g = g.loc[filter_rows(g['efficiency'], user_efficacy), :]
    g = g.loc[filter_rows(g['categ_x'], user_x), :]

##do similarit check to rank the exact search results
    total_scores_1 = []
    for index, row in g.iterrows():
      v_1 = calculate_over_all(row['categ_continent'], user_continent)
  #print(row['efficiency'])
      v_2 = calculate_over_all([row['efficiency']], user_efficacy)
  #print(row['country'])
      v_3 = calculate_over_all(row['categ_country'], user_country)
      v_4 = calculate_over_all(row['categ_category'], user_category, True)
  #print(row['categ_x'])
      v_5 = calculate_over_all([row['categ_x']], user_x)
      total_scores_1.append((0.1 * v_1+ 0.1 * v_2+0.1 * v_3+0.9*v_4+0.1* v_5))
    emp_dic_1 = {}
    k = 0
    for i in total_scores_1:
      emp_dic_1[k] = i
      k = k + 1
    sorted_dic_1 = dict(sorted(emp_dic_1.items(), key=lambda x:x[1] , reverse= True))

    if len(sorted_dic_1) >= 5:
      names = [g.iloc[int(x),1] for x in list(sorted_dic_1.keys())[0:6]]
      counts = list(sorted_dic_1.values())[0:6]
    else:
      name = [f.iloc[int(x),1] for x in list(sorted_dic.keys())[0:6]]
      counts = list(sorted_dic.values())[0:6]

##plot the 5 topmost results
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.pie(counts, labels=names, autopct='%1.1f%%')
    plt.savefig("/content/result1.png", pad_inches = 0.2, bbox_inches = 'tight')
