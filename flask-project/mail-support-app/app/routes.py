from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db, login_manager
from app.models import User
from app.forms import RegistrationForm, LoginForm

# Create a Blueprint for routes
main_routes = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_routes.route('/')
def home():
    return render_template('index.html')

@main_routes.route('/support', methods=['GET', 'POST'])
@login_required
def support():
    if request.method == 'POST':
        domain = request.form.get('domain')
        receiver_email = request.form.get('receiver_email')
        sender_email = request.form.get('sender_email')
        valid_email = request.form.get('valid_email')
        invalid_email = request.form.get('invalid_email')
        
        # Process data (e.g., save to database, interact with Barracuda API)
        flash('Your request has been submitted!', 'success')
        return redirect(url_for('routes.home'))
    return render_template('support.html')

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('routes.home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)

@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))