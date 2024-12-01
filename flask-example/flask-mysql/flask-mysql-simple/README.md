আপনি যদি XAMPP ব্যবহার করে MySQL সেটআপ করে থাকেন, তাহলে আপনার MySQL সার্ভারের হোস্টনেম সাধারণত `localhost` হবে। নিচে আমি দেখাচ্ছি কিভাবে Flask অ্যাপ্লিকেশনকে MySQL ডাটাবেজের সাথে সংযুক্ত করবেন।

### ১. প্রয়োজনীয় প্যাকেজ ইনস্টল করা

প্রথমে, Flask এবং MySQL এর সাথে সংযোগ স্থাপনের জন্য প্রয়োজনীয় প্যাকেজ ইনস্টল করুন:
```bash
pip install Flask Flask-SQLAlchemy Flask-MySQLdb python-dotenv
```

### ২. `.env` ফাইল তৈরি করা

প্রোজেক্ট ডিরেক্টরিতে `.env` নামে একটি ফাইল তৈরি করুন এবং নিচের মতো ডাটাবেজ সংযোগের তথ্য যোগ করুন:
```
DB_HOST=localhost
DB_NAME=flask_db
DB_USER=root
DB_PASS=your_mysql_password
```

### ৩. Flask অ্যাপ্লিকেশন কনফিগার করা

`app.py` ফাইলে `.env` ফাইল থেকে ডাটাবেজ সংযোগের তথ্য লোড করুন এবং Flask অ্যাপ্লিকেশন কনফিগার করুন:
```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# .env ফাইল থেকে পরিবেশ ভেরিয়েবল লোড করা
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### ৪. টেমপ্লেট তৈরি করা

`templates` নামে একটি ডিরেক্টরি তৈরি করুন এবং সেখানে `index.html` এবং `register.html` নামে দুটি ফাইল তৈরি করুন।

**index.html**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User List</title>
</head>
<body>
    <h1>Registered Users</h1>
    <ul>
        {% for user in users %}
            <li>{{ user.username }} - {{ user.email }}</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('register') }}">Register a new user</a>
</body>
</html>
```

**register.html**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <br>
        <button type="submit">Register</button>
    </form>
</body>
</html>
```

### ৫. ডাটাবেজ তৈরি করা

ডাটাবেজ তৈরি করতে নিচের কোডটি রান করুন:
```python
from app import app, db

with app.app_context():
    db.create_all()
```

### ৬. অ্যাপ্লিকেশন রান করা

অ্যাপ্লিকেশন রান করতে নিচের কমান্ডটি ব্যবহার করুন:
```bash
python app.py
```

এখন আপনার ব্রাউজারে `http://127.0.0.1:5000/` এ যান এবং আপনার অ্যাপ্লিকেশনটি দেখুন। আপনি নতুন ইউজার রেজিস্ট্রেশন করতে পারবেন এবং সেই ইউজারদের তালিকা দেখতে পারবেন।

এই স্টেপগুলো অনুসরণ করে আপনি সহজেই Flask এবং MySQL ব্যবহার করে একটি প্রাথমিক অ্যাপ্লিকেশন তৈরি করতে পারবেন এবং `.env` ফাইল ব্যবহার করে সংবেদনশীল তথ্য নিরাপদ রাখতে পারবেন[1](https://www.askpython.com/python-modules/flask/flask-mysql-database)[2](https://hevodata.com/learn/flask-mysql/). যদি আপনার আরও কোনো প্রশ্ন থাকে বা সাহায্য দরকার হয়, জানাতে পারেন!