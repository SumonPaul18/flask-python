from flask import Flask, request, redirect, url_for, session, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def check_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = check_user(email, password)
    if user:
        session['user'] = user[0]  # Assuming user ID is the first column
        return redirect(url_for('streamlit_app'))
    return 'Login Failed'

@app.route('/streamlit_app')
def streamlit_app():
    if 'user' in session:
        user_id = session['user']
        return redirect(f'http://localhost:8501?user={user_id}')
    return 'Unauthorized'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        return 'Registration Successful'
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)