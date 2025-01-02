from flask import render_template
from signin import signin

@signin.route('/signin')
def signin():
    return render_template('signin.html')