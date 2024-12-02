from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signin_signup')
def signin_signup():
    return render_template('signin_signup.html')

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    # Handle sign-in logic here
    return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    # Handle sign-up logic here
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)