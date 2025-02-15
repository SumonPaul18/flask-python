from flask import Flask, render_template, request, redirect, url_for, session
from openstack import connection
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Establish OpenStack connection for admin
admin_conn = connection.Connection(cloud='mycloud')

# Landing page
@app.route('/')
def landing_page():
    return render_template('landing_page.html')

# Create Project Page
@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        # Form data
        username = request.form['username']
        password = request.form['password']
        project_name = request.form['project_name']
        package_type = request.form['package_type']
        project_plan = request.form['project_plan']
        primary_project_id = request.form.get('primary_project_id')  # New field for primary project
        project_members = request.form.getlist('project_members')  # New field for project members

        # Create OpenStack Project and User
        project = admin_conn.identity.create_project(name=project_name)
        user = admin_conn.identity.create_user(name=username, password=password, default_project=project.id)

        # Assign primary project if specified (optional)
        if primary_project_id:
            admin_conn.identity.add_user_to_project(user.id, primary_project_id)

        # Add members to the new project
        for member in project_members:
            admin_conn.identity.add_user_to_project(member, project.id)

        # Save session for user context
        session['username'] = username
        session['project_id'] = project.id

        return redirect(url_for('manage_project', project_id=project.id))

    # Fetch existing projects for selection as primary projects
    existing_projects = admin_conn.identity.projects()
    return render_template('create_project.html', existing_projects=existing_projects)

# Manage Project Page
@app.route('/manage_project/<project_id>', methods=['GET'])
def manage_project(project_id):
    if 'username' not in session:
        return redirect(url_for('create_project'))

    username = session['username']
    user_conn = connection.Connection(
        cloud='mycloud',
        auth=dict(
            username=username,
            password='your_password_here',  # Use secure storage for passwords in production!
            project_id=project_id,
            auth_url='http://192.168.0.50:5000'
        )
    )

    # Fetch instances and other resources
    instances = user_conn.compute.servers()
    return render_template('manage_project.html', instances=instances)

# Create Instance Page
@app.route('/create_instance/<project_id>', methods=['GET', 'POST'])
def create_instance(project_id):
    if request.method == 'POST':
        instance_name = request.form['instance_name']
        image_id = request.form['image_id']
        flavor_id = request.form['flavor_id']
        network_id = request.form['network_id']

        username = session['username']
        user_conn = connection.Connection(
            cloud='mycloud',
            auth=dict(
                username=username,
                password='your_password_here',
                project_id=project_id,
                auth_url='http://192.168.0.50:5000'
            )
        )

        # Create instance with floating IP
        instance = user_conn.compute.create_server(
            name=instance_name,
            image_id=image_id,
            flavor_id=flavor_id,
            networks=[{"uuid": network_id}],
        )
        user_conn.compute.wait_for_server(instance)

        # Assign floating IP (example assumes floating IP pool exists)
        floating_ip = user_conn.network.create_ip(floating_network_id="your-floating-network-id")
        user_conn.compute.add_floating_ip_to_server(instance, floating_ip.floating_ip_address)

        return redirect(url_for('manage_project', project_id=project_id))

    return render_template('create_instance.html', project_id=project_id)

if __name__ == '__main__':
    app.run(debug=True)
