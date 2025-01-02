from flask import Blueprint

signin = Blueprint(
"signin", __name__, static_folder="static",
 template_folder="templates"
 )

@signin.route("/")
def signin_page():
    return "<h1> This is Signin Route</h1>"