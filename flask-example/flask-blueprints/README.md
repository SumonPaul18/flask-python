### ১. Blueprint কি?
Blueprint ফ্লাস্কের একটি ফিচার যা আপনাকে আপনার অ্যাপ্লিকেশনকে ছোট ছোট মডিউলে ভাগ করতে সাহায্য করে। এটি মূলত একটি মডুলার এবং পুনঃব্যবহারযোগ্য কোড স্ট্রাকচার তৈরি করতে ব্যবহৃত হয়।

### ২. কেনো Blueprint ব্যবহার করবেন?
মডুলারিটি: অ্যাপ্লিকেশনকে ছোট ছোট অংশে ভাগ করে কোডের রক্ষণাবেক্ষণ সহজ করা।
পুনঃব্যবহারযোগ্যতা: একই Blueprint বিভিন্ন অ্যাপ্লিকেশনে পুনঃব্যবহার করা যায়।
সহজ রাউটিং: বিভিন্ন রাউটিং লজিক আলাদা আলাদা ফাইলে রাখা যায়।

অবশ্যই! আমি আপনাকে ফ্লাস্ক `Blueprint` এর বেসিক থেকে অ্যাডভান্স বিষয়গুলো সহজভাবে ব্যাখ্যা করবো এবং ফাইল নেম সহ বাস্তবভিত্তিক উদাহরণ দেবো। এছাড়াও, কিভাবে রান করবেন তা দেখাবো।

### ৩. বেসিক লেভেল: `Blueprint` তৈরি ও রেজিস্টার করা

#### ধাপ ১: প্রজেক্ট স্ট্রাকচার তৈরি
প্রথমে একটি প্রজেক্ট ফোল্ডার তৈরি করুন এবং নিচের মত স্ট্রাকচার তৈরি করুন:

```plaintext
flask_app/
  user/
    __init__.py
    routes.py
  app.py
```

#### ধাপ ২: `Blueprint` তৈরি
`user/routes.py` ফাইলে নিচের কোড লিখুন:

```python
# user/routes.py
from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
def profile():
    return jsonify({"message": "User profile"})
```

#### ধাপ ৩: `Blueprint` রেজিস্টার করা
`app.py` ফাইলে নিচের কোড লিখুন:

```python
# app.py
from flask import Flask
from user.routes import user_bp

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
```

### ২. ইন্টারমিডিয়েট লেভেল: `Blueprint` এ কনফিগারেশন ও টেমপ্লেট ব্যবহার

#### কনফিগারেশন
`user/routes.py` ফাইলে কনফিগারেশন ব্যবহার করতে পারেন:

```python
# user/routes.py
from flask import Blueprint, jsonify, current_app

user_bp = Blueprint('user', __name__)

@user_bp.route('/config', methods=['GET'])
def config():
    return jsonify({"config": current_app.config['MY_CONFIG']})
```

`app.py` ফাইলে কনফিগারেশন সেট করুন:

```python
# app.py
from flask import Flask
from user.routes import user_bp

app = Flask(__name__)
app.config['MY_CONFIG'] = 'This is a config value'

app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
```

#### টেমপ্লেট ব্যবহার
`user/routes.py` ফাইলে টেমপ্লেট ব্যবহার করতে পারেন:

```python
# user/routes.py
from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')
```

`user/templates/dashboard.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- user/templates/dashboard.html -->
<!DOCTYPE html>
<html>
<head>
    <title>User Dashboard</title>
</head>
<body>
    <h1>Welcome to the User Dashboard</h1>
</body>
</html>
```

### ৩. অ্যাডভান্স লেভেল: `Blueprint` এ মডেল ও ফর্ম ব্যবহার

#### মডেল ব্যবহার
`models.py` ফাইলে মডেল তৈরি করুন:

```python
# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
```

`user/routes.py` ফাইলে মডেল ব্যবহার করুন:

```python
# user/routes.py
from flask import Blueprint, jsonify
from models import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"username": user.username, "email": user.email} for user in users])
```

`app.py` ফাইলে মডেল রেজিস্টার করুন:

```python
# app.py
from flask import Flask
from models import db
from user.routes import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

app.register_blueprint(user_bp, url_prefix='/user')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

#### ফর্ম ব্যবহার
`forms.py` ফাইলে ফর্ম তৈরি করুন:

```python
# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
```

`user/routes.py` ফাইলে ফর্ম ব্যবহার করুন:

```python
# user/routes.py
from flask import Blueprint, render_template, redirect, url_for
from forms import UserForm

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        # Form processing logic here
        return redirect(url_for('user.dashboard'))
    return render_template('create_user.html', form=form)
```

`user/templates/create_user.html` ফাইলে টেমপ্লেট তৈরি করুন:

```html
<!-- user/templates/create_user.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Create User</title>
</head>
<body>
    <h1>Create User</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.username.label }} {{ form.username() }}<br>
        {{ form.email.label }} {{ form.email() }}<br>
        {{ form.submit() }}
    </form>
</body>
</html>
```

### ৪. অ্যাপ্লিকেশন রান করা
এখন আপনার প্রজেক্ট ফোল্ডারে গিয়ে নিচের কমান্ডটি চালান:

```bash
python app.py
```

এইভাবে আপনি ফ্লাস্ক `Blueprint` ব্যবহার করে একটি সম্পূর্ণ অ্যাপ্লিকেশন তৈরি করতে পারেন। কোনো প্রশ্ন থাকলে জানাতে পারেন! 😊
