এখানে একটি সম্পূর্ণ ফ্লাস্ক প্রজেক্টের উদাহরণ দেওয়া হলো, যেখানে হোম পেজে হেডার, ফুটার, হিরো সেকশন, নেভিগেশন মেনু এবং সাইন-ইন বাটন থাকবে। সাইন-ইন বাটনে ক্লিক করলে একটি নতুন সাইন-ইন পেজ ওপেন হবে।

### প্রজেক্ট স্ট্রাকচার
```
my_flask_app/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── signin.html
│   ├── static/
│       ├── css/
│           ├── style.css
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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

from app import routes
```

#### app/routes.py
```python
from flask import render_template, url_for, redirect
from app import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')
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
    <header>
        <nav>
            <ul>
                <li><a href="{{ url_for('home') }}">Home</a></li>
                <li><a href="{{ url_for('signin') }}">Sign In</a></li>
            </ul>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2024 My Flask App</p>
    </footer>
</body>
</html>
```

#### app/templates/home.html
```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}
    <section class="hero">
        <h1>Welcome to My Flask App</h1>
        <p>This is the hero section of the home page.</p>
    </section>
{% endblock %}
```

#### app/templates/signin.html
```html
{% extends "base.html" %}
{% block title %}Sign In{% endblock %}
{% block content %}
    <h1>Sign In</h1>
    <form method="POST">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username">
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password">
        </div>
        <div>
            <button type="submit">Sign In</button>
        </div>
    </form>
{% endblock %}
```

#### app/static/css/style.css
```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

header {
    background-color: #333;
    color: #fff;
    padding: 1rem;
}

header nav ul {
    list-style: none;
    padding: 0;
}

header nav ul li {
    display: inline;
    margin-right: 1rem;
}

header nav ul li a {
    color: #fff;
    text-decoration: none;
}

.hero {
    background-color: #f4f4f4;
    padding: 2rem;
    text-align: center;
}

footer {
    background-color: #333;
    color: #fff;
    text-align: center;
    padding: 1rem;
    position: fixed;
    width: 100%;
    bottom: 0;
}
```

#### config.py
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
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
```

#### .env
```
SECRET_KEY=your_secret_key
```

## এই ফ্লাস্ক প্রজেক্টটি রান করার জন্য নিচের ধাপগুলো অনুসরণ করুন:

### ধাপ ১: প্রয়োজনীয় প্যাকেজ ইনস্টল করুন
প্রথমে, আপনার প্রজেক্ট ডিরেক্টরিতে যান এবং প্রয়োজনীয় প্যাকেজগুলি ইনস্টল করুন:
```bash
cd my_flask_app
pip install -r requirements.txt
```

### ধাপ ২: পরিবেশ ভেরিয়েবল সেট করুন
`.env` ফাইলটি তৈরি করুন এবং এতে আপনার সিক্রেট কী এবং ডাটাবেস ইউআরআই সেট করুন:
```plaintext
SECRET_KEY=your_secret_key
```

### ধাপ ৩: অ্যাপ্লিকেশন চালান
অ্যাপ্লিকেশন চালানোর জন্য `run.py` ফাইলটি চালান:
```bash
python run.py
```

### ধাপ ৪: ব্রাউজারে অ্যাপ্লিকেশন দেখুন
আপনার ব্রাউজারে যান এবং `http://127.0.0.1:5000/` ঠিকানায় অ্যাপ্লিকেশনটি দেখুন।

এই ধাপগুলি অনুসরণ করে আপনি আপনার ফ্লাস্ক প্রজেক্টটি সফলভাবে রান করতে পারবেন।

#### এই কোডগুলি একটি সম্পূর্ণ ফ্লাস্ক প্রজেক্টের উদাহরণ। আপনি এটি আপনার প্রয়োজন অনুযায়ী কাস্টমাইজ করতে পারেন।
