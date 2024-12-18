from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required, logout_user
from flask_dance.contrib.google import google
from extensions import db

# Create a Blueprint
routes = Blueprint('routes', __name__)

@routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("routes.index"))

@routes.route("/")
def index():
    google_info = None
    if current_user.is_authenticated:
        resp = google.get("/oauth2/v2/userinfo")
        if resp.ok:
            google_info = resp.json()
    return render_template("home.html", google_info=google_info)

@routes.route("/signin")
def signin():
    return render_template("signin.html")
    
    
@routes.route("/solutions")
def solutions():
    return render_template("solutions.html")