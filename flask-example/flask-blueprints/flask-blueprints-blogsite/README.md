আমরা একটি সাধারণ ব্লগ ওয়েবসাইট তৈরি করবো যেখানে ব্যবহারকারীরা নিবন্ধন করতে পারবে, লগইন করতে পারবে এবং পোস্ট তৈরি করতে পারবে। আমরা ফ্লাস্ক `Blueprints` ব্যবহার করে এই ওয়েবসাইটটি তৈরি করবো। নিচে ধাপে ধাপে প্রক্রিয়াটি ব্যাখ্যা করা হলো:

### ১. প্রজেক্ট স্ট্রাকচার তৈরি
প্রথমে একটি প্রজেক্ট ফোল্ডার তৈরি করুন এবং নিচের মত স্ট্রাকচার তৈরি করুন:

```plaintext
flask_blog/
  auth/
    __init__.py
    routes.py
    forms.py
  blog/
    __init__.py
    routes.py
    forms.py
  templates/
    auth/
      login.html
      register.html
    blog/
      create_post.html
      home.html
  models.py
  app.py
```

### ২. প্রয়োজনীয় প্যাকেজ ইনস্টল করা
প্রথমে প্রয়োজনীয় প্যাকেজগুলো ইনস্টল করুন:

```bash
pip install Flask Flask-SQLAlchemy Flask-WTF
```

### ৩. মডেল তৈরি করা
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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

### ৪. `auth` মডিউল তৈরি করা
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
            return redirect(url_for('blog.home'))
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

### ৫. `blog` মডিউল তৈরি করা
`blog/routes.py` ফাইলে রাউট তৈরি করুন:

```python
# blog/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Post, db
from blog.forms import PostForm

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def home():
    posts = Post.query.all()
    return render_template('blog/home.html', posts=posts)

@blog_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog.home'))
    return render_template('blog/create_post.html', form=form)
```

`blog/forms.py` ফাইলে ফর্ম তৈরি করুন:

```python
# blog/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
```

### ৬. টেমপ্লেট তৈরি করা
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

`templates/blog/home.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- templates/blog/home.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Home</h1>
    <a href="{{ url_for('blog.new_post') }}">Create New Post</a>
    <ul>
        {% for post in posts %}
            <li>{{ post.title }} - {{ post.content }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

`templates/blog/create_post.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- templates/blog/create_post.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Create Post</title>
</head>
<body>
    <h1>Create Post</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.title.label }} {{ form.title() }}<br>
        {{ form.content.label }} {{ form.content() }}<br>
        {{ form.submit() }}
    </form>
</body>
</html>
```

### ৭. অ্যাপ্লিকেশন রান করা
`app.py` ফাইলে নিচের কোড লিখুন:

```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User
from auth.routes import auth_bp
from blog.routes import blog_bp

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
app.register_blueprint(blog_bp, url_prefix='/')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

এখন আপনার প্রজেক্ট ফোল্ডারে গিয়ে নিচের কমান্ডটি চালান:

```bash
python app.py
```

এইভাবে আপনি ফ্লাস্ক `Blueprints` ব্যবহার করে একটি সম্পূর্ণ ব্লগ ওয়েবসাইট তৈরি করতে পারেন। কোনো প্রশ্ন থাকলে জানাতে পারেন! 😊
