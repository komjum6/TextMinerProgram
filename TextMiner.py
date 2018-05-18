from flask import Flask, render_template, request, flash
import os

app = Flask(__name__)

#De Root Map
@app.route('/')
def index():
    return render_template('home.html')
    
#De plaats waar dingen gevisualiseerd worden
@app.route('/visualisations')
def visualisations():
    return render_template('visualisations.html')

#De plaats voor sidenotes
@app.route('/notes')
def notes():
    return render_template('notes.html')

#Een plaats voor een introductie etc
@app.route('/about')
def about():
    return render_template('about.html')

#Error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)