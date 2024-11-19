from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return "Home Page"

@app.route('/signin')
def signin():
    return "Sign In / Sign Up"


if __name__ == '__main__':
    app.run(debug=True)