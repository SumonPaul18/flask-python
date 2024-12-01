অবশ্যই, আপনি Flask অ্যাপ্লিকেশনে MySQL ডাটাবেস সংযোগ করতে পারেন এবং স্বয়ংক্রিয়ভাবে ডাটাবেস ও টেবিল তৈরি করতে পারেন। এছাড়াও, আপনি একই ডাটাবেসে একাধিক টেবিল তৈরি করে ডাটা রাখতে পারবেন। নিচে ধাপগুলো দেখানো হলো:

### ধাপ ১: প্রয়োজনীয় প্যাকেজ ইনস্টল করা
```bash
pip install flask flask-sqlalchemy pymysql
```

### ধাপ ২: Flask অ্যাপ্লিকেশন কনফিগার করা
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_username:your_password@localhost/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Create database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Database and tables created successfully!"

if __name__ == '__main__':
    app.run(debug=True)
```

### ধাপ ৩: ডাটাবেস এবং টেবিল তৈরি করা
উপরের কোডে, `db.create_all()` ফাংশনটি ব্যবহার করে ডাটাবেস এবং টেবিল স্বয়ংক্রিয়ভাবে তৈরি করা হবে। আপনি `User` এবং `Post` নামে দুটি টেবিল তৈরি করেছেন।

### ধাপ ৪: একাধিক টেবিলে ডাটা রাখা
আপনি একই ডাটাবেসে একাধিক টেবিল তৈরি করে ডাটা রাখতে পারেন। উদাহরণস্বরূপ, উপরের কোডে `User` এবং `Post` নামে দুটি টেবিল তৈরি করা হয়েছে। আপনি এই টেবিলগুলোতে ডাটা যোগ করতে পারেন:

```python
@app.route('/add_user')
def add_user():
    new_user = User(username='john_doe')
    db.session.add(new_user)
    db.session.commit()
    return "User added successfully!"

@app.route('/add_post')
def add_post():
    new_post = Post(title='First Post', content='This is the content of the first post.')
    db.session.add(new_post)
    db.session.commit()
    return "Post added successfully!"
```

এই ধাপগুলো অনুসরণ করে আপনি সহজেই Flask অ্যাপ্লিকেশনে MySQL ডাটাবেস সংযোগ করতে পারবেন এবং স্বয়ংক্রিয়ভাবে ডাটাবেস ও টেবিল তৈরি করতে পারবেন। এছাড়াও, আপনি একই ডাটাবেসে একাধিক টেবিল তৈরি করে ডাটা রাখতে পারবেন। কোনো প্রশ্ন থাকলে জানাবেন!