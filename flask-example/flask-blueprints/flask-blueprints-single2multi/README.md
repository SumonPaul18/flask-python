আমি আপনাকে দেখাবো কিভাবে একটি সিংগেল কোড ফ্লাস্ক অ্যাপ্লিকেশনকে ছোট ছোট অংশে ভাগ করে `Blueprints` ব্যবহার করে মডুলার করা যায়। ধরুন, আপনার সিংগেল কোড অ্যাপ্লিকেশনটি নিচের মত:

### সিংগেল কোড অ্যাপ্লিকেশন
```python
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
```

### মডুলার অ্যাপ্লিকেশন
এখন আমরা এই অ্যাপ্লিকেশনটিকে ছোট ছোট অংশে ভাগ করবো এবং `Blueprints` ব্যবহার করবো।

#### প্রজেক্ট স্ট্রাকচার
```plaintext
flask_app/
  auth/
    __init__.py
    routes.py
    forms.py
  templates/
    auth/
      login.html
      register.html
    home.html
  models.py
  app.py
```

#### মডেল তৈরি করা
`models.py` ফাইলে মডেল তৈরি করুন:

```python
# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
```

#### `auth` মডিউল তৈরি করা
`auth/routes.py` ফাইলে রাউট তৈরি করুন:

```python
# auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User, db
from auth.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
```

`auth/forms.py` ফাইলে ফর্ম তৈরি করুন:

```python
# auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
```

#### টেমপ্লেট তৈরি করা
`templates/auth/register.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- templates/auth/register.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.username.label }} {{ form.username() }}<br>
        {{ form.email.label }} {{ form.email() }}<br>
        {{ form.password.label }} {{ form.password() }}<br>
        {{ form.confirm_password.label }} {{ form.confirm_password() }}<br>
        {{ form.submit() }}
    </form>
</body>
</html>
```

`templates/auth/login.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- templates/auth/login.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.email.label }} {{ form.email() }}<br>
        {{ form.password.label }} {{ form.password() }}<br>
        {{ form.submit() }}
    </form>
</body>
</html>
```

`templates/home.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- templates/home.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Welcome to the Home Page!</h1>
    <a href="{{ url_for('auth.logout') }}">Logout</a>
</body>
</html>
```

#### অ্যাপ্লিকেশন রান করা
`app.py` ফাইলে নিচের কোড লিখুন:

```python
# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User
from auth.routes import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return render_template('home.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

এখন আপনার প্রজেক্ট ফোল্ডারে গিয়ে নিচের কমান্ডটি চালান:

```bash
python app.py
```

এইভাবে আপনি একটি সিংগেল কোড ফ্লাস্ক অ্যাপ্লিকেশনকে ছোট ছোট অংশে ভাগ করে `Blueprints` ব্যবহার করে মডুলার করতে পারেন। কোনো প্রশ্ন থাকলে জানাতে পারেন! 😊
