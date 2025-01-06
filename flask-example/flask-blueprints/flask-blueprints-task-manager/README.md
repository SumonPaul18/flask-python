আমরা ফ্লাস্ক `Blueprints` ব্যবহার করে একটি সাধারণ টাস্ক ম্যানেজমেন্ট অ্যাপ্লিকেশন তৈরি করবো এবং ছোট ছোট অংশে ভাগ করবো। যেখানে ব্যবহারকারীরা টাস্ক তৈরি করতে, দেখতে এবং মুছতে পারবে। 

### প্রজেক্ট স্ট্রাকচার
প্রথমে একটি প্রজেক্ট ফোল্ডার তৈরি করুন এবং নিচের মত স্ট্রাকচার তৈরি করুন:

```plaintext
flask_task_manager/
  auth/
    __init__.py
    routes.py
    forms.py
  tasks/
    __init__.py
    routes.py
    forms.py
  templates/
    auth/
      login.html
      register.html
    tasks/
      create_task.html
      home.html
  models.py
  app.py
```

### ১. মডেল তৈরি করা
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

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

### ২. `auth` মডিউল তৈরি করা
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
            return redirect(url_for('tasks.home'))
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

### ৩. `tasks` মডিউল তৈরি করা
`tasks/routes.py` ফাইলে রাউট তৈরি করুন:

```python
# tasks/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Task, db
from tasks.forms import TaskForm

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks/home.html', tasks=tasks)

@tasks_bp.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('tasks.home'))
    return render_template('tasks/create_task.html', form=form)
```

`tasks/forms.py` ফাইলে ফর্ম তৈরি করুন:

```python
# tasks/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Task')
```

### ৪. টেমপ্লেট তৈরি করা
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

`templates/tasks/home.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- templates/tasks/home.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Home</h1>
    <a href="{{ url_for('tasks.new_task') }}">Create New Task</a>
    <ul>
        {% for task in tasks %}
            <li>{{ task.title }} - {{ task.description }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

`templates/tasks/create_task.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- templates/tasks/create_task.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Create Task</title>
</head>
<body>
    <h1>Create Task</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.title.label }} {{ form.title() }}<br>
        {{ form.description.label }} {{ form.description() }}<br>
        {{ form.submit() }}
    </form>
</body>
</html>
```

### ৫. অ্যাপ্লিকেশন রান করা
`app.py` ফাইলে নিচের কোড লিখুন:

```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User
from auth.routes import auth_bp
from tasks.routes import tasks_bp

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
app.register_blueprint(tasks_bp, url_prefix='/')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

এখন আপনার প্রজেক্ট ফোল্ডারে গিয়ে নিচের কমান্ডটি চালান:

```bash
python app.py
```

এইভাবে আপনি ফ্লাস্ক `Blueprints` ব্যবহার করে একটি সম্পূর্ণ টাস্ক ম্যানেজমেন্ট অ্যাপ্লিকেশন তৈরি করতে পারেন। কোনো প্রশ্ন থাকলে জানাতে পারেন! 😊
