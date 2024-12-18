from flask import Blueprint

admin_page = Blueprint(
"admin", __name__, static_folder="static",
 template_folder="templates"
 )

@admin_page.route("/admin")
def admin():
    return "<h1> This is Admin Route</h1>"

@admin_page.route("/user")
def user():
    return "<h1> This is User Route</h1>"
