from flask import Flask
from admin import admin_page
from bp.signin import signin

app = Flask(__name__)

app.register_blueprint(admin_page, url_prefix="/admin")
app.register_blueprint(signin, url_prefix="/signin")


@app.route("/")
def index():
    return "<h1> This is Home Route</h1>"

if __name__ == "__main__":
    app.run(debug=True)
