Flask অ্যাপ্লিকেশনে MySQL ডাটাবেস ব্যবহার করার জন্য বিভিন্ন পদ্ধতি রয়েছে। আমরা ইতিমধ্যে একটি পদ্ধতি দেখেছি যেখানে আমরা `flask-mysql-connector` এবং `.env` ফাইল ব্যবহার করেছি। এখন আমরা আরও কিছু পদ্ধতি এবং কিভাবে MySQL ডাটাবেস কাজ করে তা নিয়ে আলোচনা করবো।

### পদ্ধতি ১: Flask-MySQLdb ব্যবহার করা
`flask-mysqldb` একটি জনপ্রিয় প্যাকেজ যা Flask অ্যাপ্লিকেশনের সাথে MySQL ডাটাবেস সংযোগ করতে ব্যবহৃত হয়।

#### ধাপ ১: প্যাকেজ ইনস্টল করা
```bash
pip install flask-mysqldb
```

#### ধাপ ২: Flask অ্যাপ্লিকেশন কনফিগার করা
```python
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database_name'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT DATABASE()''')
    rv = cur.fetchone()
    return f'Connected to database: {rv}'

if __name__ == '__main__':
    app.run(debug=True)
```

### পদ্ধতি ২: SQLAlchemy ব্যবহার করা
SQLAlchemy একটি শক্তিশালী ORM (Object Relational Mapper) যা ডাটাবেসের সাথে কাজ করা সহজ করে তোলে।

#### ধাপ ১: প্যাকেজ ইনস্টল করা
```bash
pip install flask-sqlalchemy
```

#### ধাপ ২: Flask অ্যাপ্লিকেশন কনফিগার করা
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your_username:your_password@localhost/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/')
def index():
    users = User.query.all()
    return f'Users: {users}'

if __name__ == '__main__':
    app.run(debug=True)
```

### MySQL ডাটাবেস কিভাবে কাজ করে
MySQL একটি রিলেশনাল ডাটাবেস ম্যানেজমেন্ট সিস্টেম (RDBMS) যা ডাটাবেস তৈরি, পরিচালনা এবং ম্যানিপুলেট করতে SQL (Structured Query Language) ব্যবহার করে। MySQL ডাটাবেসে ডাটা টেবিল আকারে সংরক্ষিত হয়, যেখানে প্রতিটি টেবিলের কলাম এবং সারি থাকে।

#### সাধারণ SQL কমান্ডসমূহ:
- **SELECT**: ডাটাবেস থেকে ডাটা নির্বাচন করতে ব্যবহৃত হয়।
- **INSERT**: ডাটাবেসে নতুন ডাটা যোগ করতে ব্যবহৃত হয়।
- **UPDATE**: ডাটাবেসে বিদ্যমান ডাটা আপডেট করতে ব্যবহৃত হয়।
- **DELETE**: ডাটাবেস থেকে ডাটা মুছে ফেলতে ব্যবহৃত হয়।

উদাহরণস্বরূপ, একটি টেবিল তৈরি এবং ডাটা যোগ করার জন্য নিচের SQL কমান্ডগুলো ব্যবহার করা যেতে পারে:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

INSERT INTO users (username, email) VALUES ('john_doe', 'john@example.com');
```

এই পদ্ধতিগুলো ব্যবহার করে আপনি সহজেই Flask অ্যাপ্লিকেশনের সাথে MySQL ডাটাবেস সংযোগ করতে পারবেন এবং ডাটাবেসের সাথে কাজ করতে পারবেন। কোনো প্রশ্ন থাকলে জানাবেন!