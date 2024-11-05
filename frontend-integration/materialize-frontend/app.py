from flask import Flask,render_template
from flask_material import Material

app = Flask(__name__)
Material(app)

@app.route('/')
def index():
  return render_template("index.html")

if __name__ == '__main__':
  app run(debug=ture, host="0.0.0.0", port=5000)
