from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tarzan")
def tarzan():
    return render_template("tarzan.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)