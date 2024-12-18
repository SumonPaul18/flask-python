from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/streamlit')
def streamlit_app():
    return render_template('streamlit.html')

if __name__ == '__main__':
    app.run()
