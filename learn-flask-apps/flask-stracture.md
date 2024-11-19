# Flask প্রজেক্ট স্ট্রাকচার
```
my_flask_app/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── create_post.html
│   ├── static/
│       ├── css/
│       ├── js/
│       ├── images/
│
├── config.py
├── run.py
├── requirements.txt
├── .env
```

### কোড

#### app/__init__.py
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes
```

#### app/routes.py
```python
from flask import render_template, url_for, flash, redirect
from app import app, db
from app.forms import PostForm
from app.models import Post

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)
```

#### app/models.py
```python
from datetime import datetime
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
```

#### app/forms.py
```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
```

#### app/templates/base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>
        <ul>
            <li><a href="{{ url_for('home') }}">Home</a></li>
            <li><a href="{{ url_for('about') }}">About</a></li>
            <li><a href="{{ url_for('new_post') }}">New Post</a></li>
        </ul>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

#### app/templates/home.html
```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}
    <h1>Home Page</h1>
    {% for post in posts %}
        <article>
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
            <small>Posted on {{ post.date_posted }}</small>
        </article>
    {% endfor %}
{% endblock %}
```

#### app/templates/about.html
```html
{% extends "base.html" %}
{% block title %}About{% endblock %}
{% block content %}
    <h1>About Page</h1>
    <p>This is the about page.</p>
{% endblock %}
```

#### app/templates/create_post.html
```html
{% extends "base.html" %}
{% block title %}New Post{% endblock %}
{% block content %}
    <h1>Create New Post</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div>
            {{ form.title.label }}<br>
            {{ form.title(size=32) }}
        </div>
        <div>
            {{ form.content.label }}<br>
            {{ form.content(rows=10) }}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
{% endblock %}
```

#### config.py
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
```

#### run.py
```python
from app import app

if __name__ == '__main__':
    app.run(debug=True)
```

#### requirements.txt
```
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Bcrypt==0.7.1
Flask-WTF==0.15.1
```

#### .env
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///site.db
```

এই কোডগুলি একটি সম্পূর্ণ ফ্লাস্ক প্রজেক্টের উদাহরণ। আপনি এটি আপনার প্রয়োজন অনুযায়ী কাস্টমাইজ করতে পারেন। কোনো প্রশ্ন থাকলে জানাতে পারেন!
