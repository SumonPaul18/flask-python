import os
import uuid
import yaml
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from openstack import connection
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'  # Database for storing projects
db = SQLAlchemy(app)

# Establish OpenStack connection
conn = connection.Connection(cloud='mycloud')

# Database model for storing projects
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_username = db.Column(db.String(80), nullable=False)  # Visitor-specific identifier
    project_name = db.Column(db.String(120), nullable=False)
    project_id = db.Column(db.String(120), nullable=False)
    clouds_yaml_file = db.Column(db.String(120), nullable=False)

# Automatically initialize the database if it doesn't exist
@app.before_first_request
def initialize_database():
    """Automatically create the database and tables if they don't exist."""
    db.create_all()

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        visitor_username = request.form['username']
        session['username'] = visitor_username  # Store username in session

        project_name = request.form['project_name']
        password = request.form['password']
        location = request.form['location']

        # Create a new OpenStack project and user
        project = conn.identity.create_project(name=project_name)
        user = conn.identity.create_user(name=visitor_username, password=password, default_project=project.id)

        # Generate unique filename for clouds.yaml
        unique_filename = f"clouds_{uuid.uuid4()}.yaml"
        clouds_yaml_path = os.path.join(os.getcwd(), unique_filename)

        # Prepare and write clouds.yaml content
        clouds_yaml_content = {
            'clouds': {
                project_name: {
                    'auth': {
                        'auth_url': 'https://your-auth-url.com/v3',
                        'username': visitor_username,
                        'password': password,
                        'project_id': project.id,
                        'project_name': project_name,
                        'user_domain_name': 'Default',
                        'project_domain_name': 'Default',
                    },
                    'region_name': location,
                }
            }
        }

        with open(clouds_yaml_path, 'w') as yaml_file:
            yaml.dump(clouds_yaml_content, yaml_file)

        # Save the project in the database
        new_project = Project(
            visitor_username=visitor_username,
            project_name=project_name,
            project_id=project.id,
            clouds_yaml_file=unique_filename,
        )
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('list_projects'))

    return render_template('create_project.html')


@app.route('/list_projects', methods=['GET'])
def list_projects():
    """List all projects created by the current visitor."""
    if 'username' not in session:
        return redirect(url_for('create_project'))

    username = session['username']
    projects = Project.query.filter_by(visitor_username=username).all()
    return render_template('list_projects.html', projects=projects)


@app.route('/create_instance/<project_id>', methods=['GET', 'POST'])
def create_instance(project_id):
    """Create an instance under the current visitor's project."""
    if request.method == 'POST':
        if 'username' not in session:
            return jsonify({'error': 'User not logged in'}), 401

        data = request.form
        instance_name = data['instance_name']
        image_id = data['image_id']
        flavor_id = data['flavor_id']
        network_id = data['network_id']

        # Ensure the project belongs to the current user
        username = session['username']
        project = Project.query.filter_by(visitor_username=username, project_id=project_id).first()
        
        if not project:
            return jsonify({'error': 'Unauthorized access to this project'}), 403

        # Switch to the user's project context before creating an instance
        conn.set_project(project_id)

        instance = conn.compute.create_server(
            name=instance_name,
            image_id=image_id,
            flavor_id=flavor_id,
            networks=[{"uuid": network_id}],
        )
        
        conn.compute.wait_for_server(instance)

        return redirect(url_for('manage_instances', project_id=project_id))

    return render_template('create_instance.html', project_id=project_id)


@app.route('/manage_instances/<project_id>', methods=['GET'])
def manage_instances(project_id):
    """Manage instances under a specific project."""
    if 'username' not in session:
        return redirect(url_for('create_project'))

    username = session['username']
    project = Project.query.filter_by(visitor_username=username, project_id=project_id).first()
    
    if not project:
        return jsonify({'error': 'Unauthorized access to this project'}), 403

    # Fetch instances associated with this project (you may need to adjust based on your OpenStack setup)
    instances = conn.compute.servers()
    
    return render_template('manage_instances.html', instances=instances)


@app.route('/delete_instance/<instance_id>', methods=['DELETE'])
def delete_instance(instance_id):
    """Delete an instance."""
    conn.compute.delete_server(instance_id)
    return jsonify({'status': 'Instance deleted'})


@app.route('/start_instance/<instance_id>', methods=['POST'])
def start_instance(instance_id):
    """Start an instance."""
    conn.compute.start_server(instance_id)
    return jsonify({'status': 'Instance started'})


@app.route('/stop_instance/<instance_id>', methods=['POST'])
def stop_instance(instance_id):
    """Stop an instance."""
    conn.compute.stop_server(instance_id)
    return jsonify({'status': 'Instance stopped'})


@app.route('/reboot_instance/<instance_id>', methods=['POST'])
def reboot_instance(instance_id):
    """Reboot an instance."""
    conn.compute.reboot_server(instance_id)
    return jsonify({'status': 'Instance rebooted'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
