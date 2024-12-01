from flask import Flask
from flask_mysql_connector import MySQL
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = os.getenv('DBHOST')
app.config['MYSQL_DATABASE'] = os.getenv('DBNAME')
app.config['MYSQL_USER'] = os.getenv('DBUSER')
app.config['MYSQL_PASSWORD'] = os.getenv('DBPASS')

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DATABASE()")
    data = cursor.fetchone()
    cursor.close()
    return f"Connected to database: {data}"

if __name__ == '__main__':
    app.run(debug=True)