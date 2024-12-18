from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sidebar')
def sidebar():
    return render_template('sidebar.html')

@app.route('/split')
def split():
    return render_template('splited.html')

if __name__ == '__main__':
    app.run(debug=True)