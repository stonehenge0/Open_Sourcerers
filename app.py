from flask import Flask, render_template, request
import os
import analysis

## constants 
app = Flask(__name__, static_folder='docs/static', template_folder='docs')

# placeholder-dicts
result_padded = {
        "name":'name',
        "category_g":'General Category',
        "category_s":'Specific Category',
        "xcrisis":"yes or no",
        "country":"country",
        "continent":"continent",
        "efficiency":1,
        "evaluator":"Example Evaluator",
        "link_website":"https://studentenwohnheim-forum.de/",
        "link_cost":"https://studentenwohnheim-forum.de/spenden/",
        "e_title" : 'Low Impact',
        'e_text' : 'The charity evaluator found insufficient evidence or insufficient demonstrable impact on its target area leading to a lack of effectivemess data.'
    }
data = {
    'answer1':'answer1',
    'answer2':'answer2',
    'answer3':'answer3',
    'answer4':'answer4',
    'answer5':'answer5',
    'answer6':'answer6'
}

## functions
# add info to result
def pad_result(result: dict):
    """add explanation of the efficiency score to the result-dict"""
    result_padded = result
    if result_padded['efficiency'] == 1:
        result_padded["e_title"] = 'Low Impact'
        result_padded['e_text'] = f'''The charity evaluator { result_padded['evaluator'] } found insufficient evidence or insufficient demonstrable impact on its target area leading to a lack of effectivemess data.'''
    elif result_padded['efficiency'] == 2:
        result_padded['e_title'] = 'Exploratory'
        result_padded['e_text'] = f'''The charity evaluator { result_padded['evaluator'] } sees potential for impact in { result_padded['name'] }. However, they need additional evidence or research for a better evaluation. This might change with a future evaluation.'''
    elif result_padded['efficiency'] == 3:
        result_padded['e_title'] = 'Promising Impact'
        result_padded['e_text'] = f'''According to { result_padded['evaluator'] } { result_padded['name'] } demonstrates potential effectiveness, but does not belong to the top-rated. { result_padded['name'] } is regularly in evaluated and improved.''' 
    elif result_padded['efficiency'] == 4:
        result_padded['e_title'] = 'Top-rated Impact'
        result_padded['e_text'] = f'''{ result_padded['name'] } is recognized as highly effective and impactful by { result_padded['evaluator'] }'''
    return result_padded

# convert charity info to pretty html 
def result_to_html(data, result_padded):
    """rewrite the result.html with the info of the best match"""
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
        <img src="static/mosquito.png" alt="Mosquito" style="width:100%" title = "Distributing low cost nets to guard against mosquito bites to prevent malaria infections.">
    </div>
    </div>
    <div class="w3-half l3 m6 w3-margin-bottom">
    <div class="w3-display-container">
        <br>
        <br>
        <br>
        <p>active in { result_padded['country'] }, {result_padded['continent']}</p>
        <br>
        <p>with an efficieny rating of { result_padded['efficiency'] }</p>
        <p>{ result_padded['e_title'] }</p>
        <p>{ result_padded['e_text'] }</p>
        <p>More info on the efficiency and cost <a target="_blank" rel="noopener noreferrer" href={ result_padded['link_cost'] }>here</a></p>
        <br>
        <p>Does { result_padded['name'] } work to prevent an existential crisis for humanity (f.e. climate change, nuclear war)? { result_padded['xcrisis'] }</p>
        <br>
        <p>More info about the charity <a target="_blank" rel="noopener noreferrer" href={ result_padded['link_website'] }>here</a></p>
        <br>     
    </div>
    </div>   
</div>

<!-- Dynamic visualisation -->
<div class="w3-row-padding">
    <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Some dynamic visualization here</h3>
    <div class="w3-content">
    <div class="w3-display-container">
        <img src="static/Apfelkuchen.jpg" alt="Apfelkuchen" style="width:100%" title="Placeholder Apfelkuchen">
        <p>This text will be replaced with a description of the visualization.</p>
    </div>
    </div>
    
</div>     

<!-- Given Answers -->
<div class="w3-row-padding">
    <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16"></h3>
    <div class="w3-display-container">
        <div class="w3-display-topleft w3-light-grey w3-padding">Submitted Preferences</div>
        <br>
        <br>
        <h5>Where should the charity be active?</h5>
        <p>{ data['a_continent'] }</p>
        <h5>In which country should the charity be active?</h5>
        <p>{ data['a_country'] }</p>
        <h5>What should the charity work on in general?</h5>
        <p>{ data['a_topic_g'] }</p>
        <h5>What should the charity work on more specifically?</h5>
        <p>{ data['a_topic_s'] }</p>
        <h5>Do you want to apply the x-crisis filter?</h5>
        <p>{ data['xcrisis'] }</p>
        <h5>On a scale of 1 to 5, how important is cost-efficiency to you?</h5>
        <p>{ data['efficiency'] }</p>
    </div>
    <a href="questionnaire.html" class="w3-button w3-black w3-section"> Try Again</a>
    </div>




<!-- Image of location/map -->
<div class="w3-container">
    <img src="static/people_world.jpg" class="w3-image" style="width:100%" title="Image by Freepik: https://www.freepik.com/free-vector/character-illustration-diverse-people-world_3585388.htm#query=people%20around%20the%20world&position=5&from_view=search&track=ais&uuid=1be823e1-28b7-4059-842d-dd76c3b4d1b9">
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
    """render the landing page/index of the website"""
    return render_template('index.html')

# questionnaire
@app.route('/questionnaire.html')
def questionnaire():
    """render the questionnaire website"""
    return render_template('questionnaire.html')

@app.route('/submit_questionnaire', methods = ['POST'])
def submit_questionnaire():
    """handle and pad the data from the questionnaire, render result website"""
    if request.method == 'POST':
        data=request.form.to_dict()     # get the data from the http POST-method into a dict
        result = analysis.produce_result()      # get the result from the analysis-algorithm
        result_padded = pad_result(result)      # add info about the efficiency rating
        result_to_html(data, result_padded)     # rewrite the result.html with the info above
        return render_template('result.html')
    
@app.route('/try_again')
def try_again():
    """return to questionnaire website"""
    back_to_q = app.redirect("questionnaire.html", code=302)
    return back_to_q

# help page
@app.route('/help.html')
def help():
    """render help website"""
    return render_template('help.html')



if __name__=='__main__':
    app.run(debug=True, host='localhost', port=5000)