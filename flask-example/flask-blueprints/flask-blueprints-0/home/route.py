from flask import render_template
from home import home

@home.route('/home')
def homepage():
    return render_template('home.html')