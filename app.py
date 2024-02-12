from flask import Flask, render_template, request
import json
 
app = Flask(__name__, static_folder='docs/static', template_folder='docs')
 
@app.route('/' or '/index')
def index():
    return render_template('index.html')


# questionnaire
@app.route('/questionnaire.html')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/submit_questionnaire', methods = ['POST'])
def submit_questionnaire():
    if request.method == 'POST':
        a1 = request.form['answer1']
        return render_template('result.html', data=request.form)
    
@app.route('/try_again')
def try_again():
    back_to_q = app.redirect("questionnaire.html", code=302)
    return back_to_q

# help page
@app.route('/help.html')
def help():
    return render_template('help.html')


app.run(host='localhost', port=5000)