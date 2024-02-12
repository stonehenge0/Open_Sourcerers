from flask import Flask, render_template, request, flash
 
app = Flask(__name__, template_folder='docs')
 
@app.route('/')
def form():
    return render_template('questionnaire.html')

@app.route('/submit_questionnaire', methods = ['POST', 'GET'])
def submit_questionnaire():
    if request.method == 'POST':
        q_answer2 = request.form['answer2']
        if not q_answer2 == "Friend":
            flash('You answered. Yay!')


app.run(host='localhost', port=5000)