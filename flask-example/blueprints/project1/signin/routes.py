from signin import signin
from flask import render_template

@signin.route('/signin')
def signin():
    return render_template('index.html')