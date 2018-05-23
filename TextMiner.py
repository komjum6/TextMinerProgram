from flask import Flask, render_template, request, flash
import os

app = Flask(__name__)

#De Root Map
@app.route('/')
def index():
    return render_template('index.html')
    
#De plaats waar dingen gevisualiseerd worden
@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html')

#De plaats voor contact info
@app.route('/contact')
def contact():
    return render_template('contact.html')

#Een plaats voor een introductie etc
@app.route('/about')
def about():
    return render_template('about.html')
