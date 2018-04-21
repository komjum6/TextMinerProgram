from flask import Flask, render_template
#from wtforms import Form, BooleanField, StringField, PasswordField, validators
#from flask_frozen import Freezer
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/inputFile')
def inputFile():
    return render_template('inputFile.html')

@app.route('/visualisations')
def visualisations():
    return render_template('visualisations.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

import webbrowser

# Ga naar de plaats waar de webpagina geopend wordt
url = 'http://127.0.0.1:5000/'
webbrowser.open(url)

if __name__ == "__main__":
    app.run(debug=False)