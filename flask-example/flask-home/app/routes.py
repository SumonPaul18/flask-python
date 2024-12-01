from flask import render_template, url_for, redirect
from app import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')