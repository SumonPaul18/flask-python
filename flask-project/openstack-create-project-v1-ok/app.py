from flask import Flask, render_template, request, redirect, url_for
from openstack import connection
from openstack.exceptions import ConflictException

app = Flask(__name__)

# Initialize OpenStack connection (replace with your details)
conn = connection.Connection(cloud='openstack')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        try:
            conn.identity.create_project(name=project_name)
            return redirect(url_for('home'))
        except ConflictException:
            error_message = f"A project with the name '{project_name}' already exists."
            return render_template('create_project.html', error=error_message)
    return render_template('create_project.html')

if __name__ == '__main__':
    app.run(debug=True)
