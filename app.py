from flask import Flask, render_template, request
import os
import analysis
import doing_search
import pandas as pd
import numpy as np

## constants 
app = Flask(__name__, static_folder='docs/static', template_folder='docs')


## functions
 
## url handling
@app.route('/')
@app.route('/index.html')
def index():
    """Renders the landing page/index of the website."""
    return render_template('index.html')

# random charity
@app.route('/random')
def random():
    """Requests a random charity from the database, pads it with info about the efficiency score and renders the result html."""
    dataset = pd.read_csv(os.path.join(os.getcwd(),"data", "final_cleaned_meaningful_all.csv"))
    dataset_rand = dataset.sample()
    data = {
    'a_continent': dataset_rand['name'],
    'a_country':dataset_rand['country'],
    'a_topic_g':dataset_rand['category'],
    'a_topic_s':dataset_rand['category'],
    'xcrisis':dataset_rand['x-crisis'],
    'efficiency':dataset_rand['efficiency']
    }
    result = analysis.produce_random()      # get a random charity from the analysis-algorithm
    result_padded = pad_result(result)      # add info about the efficiency rating
    result_to_html(data, result_padded)     # rewrite the result.html with the info above
    return render_template('result.html')

# questionnaire
@app.route('/questionnaire.html')
def questionnaire():
    """Renders the questionnaire html."""
    country = pd.read_csv(os.path.join(os.getcwd(),"data", "country_levels.csv"))
    category = pd.read_csv(os.path.join(os.getcwd(),"data","category_levels.csv"))
    continent = pd.read_csv(os.path.join(os.getcwd(),"data","continent_levels.csv"))
    countries = country['country'].to_list()
    countries_id = country['levels'].to_list()
    len_count = len(countries_id)
    continents = continent['continent'].to_list()
    continents_id = continent['levels'].to_list()
    len_con = len(continents_id)
    categories = category['category'].to_list()
    categories_id = category['meaningful_levels'].to_list()
    len_cate = len(categories_id)
    print(len_cate)
    print(type(len_cate))
    return render_template('questionnaire.html', 
    countries = countries, countries_id = countries_id, len_count = len_count,
    		continents = continents, continents_id = continents_id, len_con = len_con
    	, categories = categories, categories_id = categories_id, len_cate = len_cate)

@app.route('/submit_questionnaire', methods = ['POST'])
def submit_questionnaire():
    """Handles and pads the data from the questionnaire, renders the result html."""
    if request.method == 'POST':
        data=request.form.to_dict()     # get the data from the http POST-method into a dict
        data_continent = request.form.getlist('a_continent')
        w_count = int(data['country_radio'])
        w_cont = int(data['continent_radio'])
        w_categ = int(data['category_radio'])
        print("here")
        print(type(w_categ))
        w_eff = int(data['eff_radio'])
        w_xcrisis = int(data['xcrisis_radio'])
        print(type(w_count))
        weights = [w_count, w_cont, w_categ, w_eff, w_xcrisis]
        data_country = request.form.getlist('a_country')
        data_category_g = request.form.getlist('a_topic_g')
        data_category_s = request.form.getlist('a_topic_s')
        data_category = data_category_g +data_category_s
        data_category = set(data_category)
        data_category = list(data_category)
        data_x = data['xcrisis']
        data_eff = data['efficiency']
        country = pd.read_csv(os.path.join(os.getcwd(),"data", "country_levels.csv"))
        category = pd.read_csv(os.path.join(os.getcwd(),"data","category_levels.csv"))
        continent = pd.read_csv(os.path.join(os.getcwd(),"data","continent_levels.csv"))
        data_user_cont = search_over(continent,data_continent,0)
        data_user_count = search_over(country,data_country,2)
        data_user_categ = search_over(category,data_category,1)
                
        #data = {'a_continent' : data_continent, 'a_country' : data_country, 'a_category' : data_category,
        	#'xcrisis' : data_x, 'efficiency' : data_eff, 'img_url' : plot_url}
        result, plot_url = doing_search.main(data_continent,data_country
        	,data_category,data_x, data_eff, weights)	# get the result from the analysis-algorithm
        data = {'a_continent' : data_user_cont, 'a_country' : data_user_count, 'a_category' : data_user_categ,
        	'xcrisis' : data_x, 'efficiency' : data_eff, 'img_url' : plot_url}
        result_padded = result      	# add info about the efficiency rating
        #result_to_html(data, result_padded,'dfg') 
        #print(result['result1'])    	# rewrite the result.html with the info above
        return render_template('result1.html', data = data, result_padded = result_padded)
    
@app.route('/try_again')
def try_again():
    """Redirects the user to the questionnaire."""
    back_to_q = app.redirect("questionnaire.html", code=302)
    return back_to_q

# help page
@app.route('/help.html')
def help():
    """Renders help html."""
    return render_template('help.html')

def search_over(temp,vec,mode):
    emp = []
    if mode == 1:
      for i in vec:
        for j_index,j in enumerate(temp.iloc[:,2].to_list()):
        #print(type(j))
        #print(type(i))
          if int(i) == int(j):
            emp.append(temp.iloc[j_index,0])
            break
    elif mode == 0:
      for i in vec:
        for j_index,j in enumerate(temp.iloc[:,1].to_list()):
          if int(i) == int(j):
            emp.append(temp.iloc[j_index,0])
            break
    elif mode == 2:
      for i in vec:
        for j_index,j in enumerate(temp.iloc[:,2].to_list()):
          if int(i) == int(j):
            emp.append(temp.iloc[j_index,1])
            break
    return(emp)



if __name__=='__main__':
    app.run(debug=True, host='localhost', port=5000)
