from flask import render_template, request, redirect, url_for
from . import signin

@signin.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # এখানে সাইন-ইন লজিক যোগ করুন
        return redirect(url_for('home.homepage'))
    return render_template('signin.html')