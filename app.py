from flask import Flask, render_template, request
import os
import doing_search
import analysis

## constants 
app = Flask(__name__, static_folder='docs/static', template_folder='docs')


## functions
# add info to result
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

# convert charity info to pretty html 
def result_to_html(data, result1_padded, result2_padded, result3_padded):
    """This function rewrites the html-template in RESULT_HTML with the info of the 3 best matches."""
    with open(os.path.join(os.getcwd(),'docs','result.html'), 'w') as f:        # dynamic, cross-plattform path
        data = data
        result_padded = result_padded
        RESULT_HTML = f"""<!DOCTYPE html>
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
    <p>The 3 charity that fit your preferences best are:</p>
    <div class="w3-col l3 m6 w3-margin-bottom">
    <div class="w3-display-container">
      <div class="w3-display-topleft w3-black w3-padding">{result1_padded['name']}</div>
    </div>
    </div>
    <div class="w3-col l3 m6 w3-margin-bottom">
    <div class="w3-display-container">
        <br>
        <br>
        <br>
        <p>active in {result1_padded['country']}, {result1_padded['continent']}</p>
        <br>
        <p>with an efficieny rating of {result1_padded['efficiency']}</p>
        <p>{result1_padded['e_title']}</p>
        <p>{result1_padded['e_text']}</p>
        <p>More info on the efficiency and cost <a target="_blank" rel="noopener noreferrer" href={result1_padded['link_cost']}>here</a></p>
        <br>
        <p>Does {result1_padded['name']} work to prevent an existential crisis for humanity (f.e. climate change, nuclear war)? 
          <br> {result1_padded['xcrisis']}</p>
        <br>
        <p>More info about the charity <a target="_blank" rel="noopener noreferrer" href={result1_padded['link_website']}>here</a></p>
        <br>     
    </div>
    </div> 
    <div class="w3-col l3 m6 w3-margin-bottom">
      <div class="w3-display-container">
        <div class="w3-display-topleft w3-black w3-padding">{result2_padded['name']}</div>
      </div>
      </div>
      <div class="w3-col l3 m6 w3-margin-bottom">
      <div class="w3-display-container">
          <br>
          <br>
          <br>
          <p>active in {result2_padded['country']}, {result2_padded['continent']}</p>
          <br>
          <p>with an efficieny rating of {result1_padded['efficiency']}</p>
          <p>{result2_padded['e_title']}</p>
          <p>{result2_padded['e_text']}</p>
          <p>More info on the efficiency and cost <a target="_blank" rel="noopener noreferrer" href={result2_padded['link_cost']}>here</a></p>
          <br>
          <p>Does {result2_padded['name']} work to prevent an existential crisis for humanity (f.e. climate change, nuclear war)? 
            <br> {result2_padded['xcrisis']}</p>
          <br>
          <p>More info about the charity <a target="_blank" rel="noopener noreferrer" href={result2_padded['link_website']}>here</a></p>
          <br>     
      </div>
      </div> 
      <div class="w3-col l3 m6 w3-margin-bottom">
        <div class="w3-display-container">
          <div class="w3-display-topleft w3-black w3-padding">{result3_padded['name']}</div>
        </div>
        </div>
        <div class="w3-col l3 m6 w3-margin-bottom">
        <div class="w3-display-container">
            <br>
            <br>
            <br>
            <p>active in {result3_padded['country']}, {result3_padded['continent']}</p>
            <br>
            <p>with an efficieny rating of {result3_padded['efficiency']}</p>
            <p>{result3_padded['e_title']}</p>
            <p>{result3_padded['e_text']}</p>
            <p>More info on the efficiency and cost <a target="_blank" rel="noopener noreferrer" href={result3_padded['link_cost']}>here</a></p>
            <br>
            <p>Does {result3_padded['name']} work to prevent an existential crisis for humanity (f.e. climate change, nuclear war)? 
              <br> {result3_padded['xcrisis']}</p>
            <br>
            <p>More info about the charity <a target="_blank" rel="noopener noreferrer" href={result3_padded['link_website']}>here</a></p>
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
        <p>{data['a_continent']}</p>
        <h5>In which country should the charity be active?</h5>
        <p>{data['a_country']}</p>
        <h5>What should the charity work on in general?</h5>
        <p>{data['a_topic_g']}</p>
        <h5>What should the charity work on more specifically?</h5>
        <p>{data['a_topic_s']}</p>
        <h5>Do you want to apply the x-crisis filter?</h5>
        <p>{data['xcrisis']}</p>
        <h5>On a scale of 1 to 5, how important is cost-efficiency to you?</h5>
        <p>{data['efficiency']}</p>
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
</html>  """
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
    data = {
    'a_continent':'Random Charity',
    'a_country':'Random Charity',
    'a_topic_g':'Random Charity',
    'a_topic_s':'Random Charity',
    'xcrisis':'Random Charity',
    'efficiency':'Random Charity'
    }
    result = analysis.produce_random()      # get a random charity from the analysis-algorithm
    result_padded = pad_result(result)      # add info about the efficiency rating
    result_to_html(data, result_padded)     # rewrite the result.html with the info above
    return render_template('result.html')

# questionnaire
@app.route('/questionnaire.html')
def questionnaire():
    """Renders the questionnaire html."""
    return render_template('questionnaire.html')

@app.route('/submit_questionnaire', methods = ['POST'])
def submit_questionnaire():
    """Handles and pads the data from the questionnaire, renders the result html."""
    if request.method == 'POST':
        data=request.form.to_dict()     # get the data from the http POST-method into a dict
        result = doing_search.main()      # get the result from the analysis-algorithm
        result1 = result['result1']
        result2 = result['result2']
        result3 = result['result3']
        result1_padded = pad_result(result1)      # add info about the efficiency rating
        result2_padded = pad_result(result2)
        result3_padded = pad_result(result3)
        result_to_html(data, result1_padded, result2_padded, result3_padded)     # rewrite the result.html with the result info
        return render_template('result.html')
    
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



if __name__=='__main__':
    app.run(debug=True, host='localhost', port=5000)