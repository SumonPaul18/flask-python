import os
import re
from flask import Flask, redirect, url_for, flash, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersekrit")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///signup-split.db"
db = SQLAlchemy(app)

# User model definition
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False)
    
# OAuth model definition for Google login
class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

# Setup Flask-Login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Setup Google OAuth blueprint
blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="dashboard"
)
blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)
app.register_blueprint(blueprint, url_prefix="/login")

# Email configuration using Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 587  # TLS port
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

def send_email(to, subject, template):
    msg = Message(subject=subject, recipients=[to], html=template)
    mail.send(msg)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email)

def confirm_token(token):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(token)
    except SignatureExpired:
        return False  # Token expired
    return email

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email address already exists. Please use a different email.")
            return redirect(url_for("signup"))

        # Password complexity check...
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', password):
            flash("Password must be at least 8 characters long and include uppercase letters, lowercase letters, numbers, and special characters.")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Send confirmation email
        token = generate_confirmation_token(email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        send_email(email, "Please confirm your email", html)

        flash("Signup successful! Please check your email to confirm your account.")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = confirm_token(token)
    except SignatureExpired:
        flash("The confirmation link has expired.")
        return redirect(url_for("signup"))
    
    user = User.query.filter_by(email=email).first_or_404()
    
    if user.confirmed:
        flash("Account already confirmed. Please login.")
        return redirect(url_for("login"))
    
    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    
    flash("You have confirmed your account. Thanks!")
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            if not user.confirmed:
                flash("Please confirm your email address first.")
                return redirect(url_for("login"))
            
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("dashboard"))
        
        flash("Login failed. Check your email and password.")
    
    return render_template("login.html")

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = generate_confirmation_token(user.email)
            reset_url = url_for('reset_password_token', token=token, _external=True)
            html = render_template('reset_password_email.html', reset_url=reset_url)
            send_email(user.email, "Password Reset Request", html)
            flash("Password reset email sent. Please check your inbox.")
        
        else:
            flash("Email not found.")
    
    return render_template("reset_password.html")

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password_token(token):
    try:
        email = confirm_token(token)
    except SignatureExpired:
        flash("The reset link has expired.")
        return redirect(url_for("reset_password"))
    
    user = User.query.filter_by(email=email).first_or_404()
    
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("reset_password_token", token=token))
        
        hashed_password = generate_password_hash(password)
        user.password = hashed_password
        
        db.session.commit()
        
        flash("Your password has been updated!")
        return redirect(url_for("login"))
    
    return render_template("reset_password_token.html", token=token)

@app.route("/")
def index():
    google_info = None
    
    if current_user.is_authenticated:
        resp = google.get("/oauth2/v2/userinfo")
        
        if resp.ok:
            google_info = resp.json()
    
    return render_template("home.html", google_info=google_info)

@app.route('/dashboard')
@login_required  # Ensure the user is logged in to access the dashboard 
def dashboard():
     return render_template('body.html')

if __name__ == "__main__":
     with app.app_context():
         db.create_all()  # Create database tables on startup 
     app.run(debug=True)  # Run the application in debug mode 
