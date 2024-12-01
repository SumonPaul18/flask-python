from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure SQLAlchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
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

if __name__ == '__main__':
    app.run(debug=True)