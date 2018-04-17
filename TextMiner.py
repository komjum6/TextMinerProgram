
# coding: utf-8

# In[ ]:

from flask import Flask, render_template
#from wtforms import Form, BooleanField, StringField, PasswordField, validators
#from flask_frozen import Freezer
app = Flask(__name__)

@app.route('/')
def to_home():
    return render_template('login.html')


import webbrowser

# Ga naar de plaats waar de webpagina geopend wordt
url = 'http://127.0.0.1:5000/'
webbrowser.open(url)

if __name__ == "__main__":
    app.run(debug=False)

