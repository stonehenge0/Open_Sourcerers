from flask import Flask, render_template, request
app = Flask(__name__)

# So this says what URL should trigger our code. Buuut this
#isn't a URL, its just a backslash

# This renders the template for the form.
@app.route("/") #from the root path go there (that's why here the "/" I think. Weil 127.../, der Slash kommt da dran)
def index():
    return render_template("form.html")

# Takes in data, calculates and then renders the calculate template.
@app.route("/calculate.html", methods=["POST"]) #Maybe this also needs to change?
def calculate():
    number = int(request.form["number"])
    result  = number * 2
    return render_template ("calculate.html", result = result)

if __name__ == "__main__":
    app.debug = True
    app.run()

