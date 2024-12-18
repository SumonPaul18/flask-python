from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', content='home')

@app.route('/section1')
def section1():
    return render_template('index.html', content='section1')

@app.route('/section2')
def section2():
    return render_template('index.html', content='section2')

@app.route('/section3')
def section3():
    return render_template('index.html', content='section3')

@app.route('/subitem1')
def subitem1():
    return render_template('index.html', content='subitem1')

@app.route('/subitem2')
def subitem2():
    return render_template('index.html', content='subitem2')

if __name__ == '__main__':
    app.run(debug=True)