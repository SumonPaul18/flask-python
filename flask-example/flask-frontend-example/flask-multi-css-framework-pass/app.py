from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/form')
def form():
    return render_template('form.html')
    
@app.route('/navbar')
def navbar():
    return render_template('navbar.html')
    
    
@app.route('/navbar1')
def navbar1():
    return render_template('navbar1.html')

if __name__ == '__main__':
    app.run(debug=True)