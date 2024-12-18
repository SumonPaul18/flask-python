from flask import Flask
from signin import signin
from home import home

app = Flask(__name__)
# Register Blueprints
app.register_blueprint(signin,url_prefix="/signin")
app.register_blueprint(home)

if __name__ == '__main__':
    app.run(debug=True)