from flask import Flask, render_template

app = Flask(__name__)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        # Here you would typically save the data to a database
        return redirect(url_for('success'))
    return render_template('create_account.html')

@app.route('/success')
def success():
    return "Account created successfully!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)