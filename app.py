from flask import Flask, render_template, request
import os
import analysis
import doing_search
import pandas as pd
import numpy as np
import ast

## constants 
app = Flask(__name__, static_folder='docs/static', template_folder='docs')


## functions
def pad_result(result: dict):
    """Add explanation of the efficiency score to the result-dict.
    Input: dict with the data of the result charity
    Output: dict with the data of the result charity AND an explanation of the efficiency score
    """
    result_padded = result
    if result_padded['efficiency'] == 1:
        result_padded["e_title"] = 'Low Impact'
        result_padded['e_text'] = f'''The charity evaluator {result_padded['evaluator']} found insufficient evidence or insufficient demonstrable impact on its target area leading to a lack of effectivemess data.'''
    elif result_padded['efficiency'] == 2:
        result_padded['e_title'] = 'Exploratory'
        result_padded['e_text'] = f'''The charity evaluator {result_padded['evaluator']} sees potential for impact in {result_padded['name']}. However, they need additional evidence or research for a better evaluation. This might change with a future evaluation.'''
    elif result_padded['efficiency'] == 3:
        result_padded['e_title'] = 'Promising Impact'
        result_padded['e_text'] = f'''According to {result_padded['evaluator']} {result_padded['name']} demonstrates potential effectiveness, but does not belong to the top-rated. {result_padded['name']} is regularly in evaluated and improved.''' 
    elif result_padded['efficiency'] == 4:
        result_padded['e_title'] = 'Top-rated Impact'
        result_padded['e_text'] = f'''{result_padded['name']} is recognized as highly effective and impactful by {result_padded['evaluator']}'''
    return result_padded


def result_to_html(data, result_padded):
    """This function rewrites the html-template in RESULT_HTML with the info of the best match."""
    with open(os.path.join(os.getcwd(),'docs','result.html'), 'w') as f:        # dynamic, cross-plattform path
        data = data
        result_padded = result_padded
        RESULT_HTML = f""" <!DOCTYPE html>
<html>
<head>
<title>ApplePy Your Result</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="static/Architect_stylesheet_W3.css">
</head>
<body>

<!-- Navbar (sit on top) -->
<div class="w3-top">
<div class="w3-bar w3-white w3-wide w3-padding w3-card">
    <a href="index.html" class="w3-bar-item w3-button"><b>ApplePy</b> Charity Finder</a>
    <!-- Float links to the right. Hide them on small screens -->
    <div class="w3-right w3-hide-small">
    <a href="index.html#example_charities" class="w3-bar-item w3-button">Example Charities</a>
    <a href="index.html#about" class="w3-bar-item w3-button">About</a>
    <a href="index.html#contact" class="w3-bar-item w3-button">Contact</a>
    <a class="w3-bar-item w3-button" href="help.html">Help</a>
    </div>
</div>
</div>

<!-- Header -->
<header class="w3-display-container w3-content w3-wide" style="max-width:1500px;" id="home">
<img class="w3-image" src="static/hands.jpg" alt="hands reaching in the air" width="1500" height="800" title="Image by Freepik: https://www.freepik.com/free-vector/love-hands_783704.htm#query=donation&position=7&from_view=search&track=sph&uuid=e9f82470-2023-4264-91ea-6eb74a19287e">
<div class="w3-display-middle w3-margin-top w3-center">
    <h1 class="w3-xxlarge w3-text-white"><span class="w3-padding w3-black w3-opacity-min"><b>ApplePy</b></span> <span class="w3-hide-small w3-text-dark-grey">Your Result</span></h1>
</div>
</header>

<!-- Page content -->
<div class="w3-content w3-padding" style="max-width:1564px">

<!-- Best Fitting Charities Section -->
<div class="w3-container w3-padding-15" id="about">
    <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Your Result</h3>
    <p>The charity that fits your preferences best is:</p>
    <div class="w3-half l3 m6 w3-margin-bottom">
    <div class="w3-display-container">
        <div class="w3-display-topleft w3-black w3-padding">{ result_padded['name'] }</div>
        <img src="static/Apfelkuchen.jpg" alt="Mosquito" style="width:100%" title = "Distributing low cost nets to guard against mosquito bites to prevent malaria infections.">
    </div>
    </div>
    <div class="w3-half l3 m6 w3-margin-bottom">
    <div class="w3-display-container">
        <br>
        <br>
        <br>
        <p>active in { result_padded['country'] }, in {result_padded['continent']} continent(s)</p>
        <br>
        <p>with an efficieny rating of { result_padded['efficiency'] }</p>
        <p>{ result_padded['e_title'] }</p>
        <p>{ result_padded['e_text'] }</p>
        <p>More info on the efficiency and cost <a target="_blank" rel="noopener noreferrer" href={ result_padded['evaluation'] }>here</a></p>
        <br>
        <p>Does { result_padded['name'] } work to prevent an existential crisis for humanity (f.e. climate change, nuclear war)? { result_padded['x-crisis'] }</p>
        <br>
        <p>More info about the charity <a target="_blank" rel="noopener noreferrer" href={ result_padded['website'] }>here</a></p>
        <br>     
    </div>
    </div>   
</div>


<!-- End page content -->
</div>

<!-- Footer -->
<footer class="w3-center w3-black w3-padding-16">
<p>Powered by <a href="https://www.w3schools.com/w3css/default.asp" title="W3.CSS" target="_blank" class="w3-hover-text-green">w3.css</a></p>
</footer>
</body>
</html> """
        f.write(RESULT_HTML)
 
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
    if dataset_rand['x-crisis'].to_list()[0] == 'n':
    	dataset_rand['x-crisis'] = 'No'
    else:
    	dataset_rand['x-crisis'] = 'Yes'
    data = {
    'name': dataset_rand['name'].to_list()[0],
    'continent': dataset_rand['continent'].to_list(),
    'country':dataset_rand['country'].to_list(),
    'category':dataset_rand['category'].to_list(),
    'a_topic_s':dataset_rand['category'].to_list(),
    'x-crisis':dataset_rand['x-crisis'].to_list()[0],
    'efficiency':int(dataset_rand['efficiency']),
    'evaluator': dataset_rand['evaluator'].to_list()[0],
    'website' : dataset_rand['website'].to_list()[0],
    'evaluation' : dataset_rand['evaluation'].to_list()[0]
    }
    print(int(data['efficiency']))
    result_padded = pad_result(data)      # add info about the efficiency rating
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
