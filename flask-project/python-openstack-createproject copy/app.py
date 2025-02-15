import os
import uuid
import yaml  # Ensure PyYAML is installed: pip install pyyaml
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from openstack import connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Establish OpenStack connection
conn = connection.Connection(cloud='mycloud')

# Store user projects and instances in memory for demonstration purposes (use a database in production)
user_projects = {}
user_instances = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        username = request.form['username']
        password = request.form['password']
        location = request.form['location']

        # Create a new project
        project = conn.identity.create_project(name=project_name)

        # Create a user and assign them to the project
        user = conn.identity.create_user(name=username, password=password, default_project=project.id)

        # Generate unique filename for clouds.yaml
        unique_filename = f"clouds_{uuid.uuid4()}.yaml"
        clouds_yaml_path = os.path.join(os.getcwd(), unique_filename)

        # Prepare the clouds.yaml content
        clouds_yaml_content = {
            'clouds': {
                project_name: {
                    'auth': {
                        'auth_url': 'http://192.168.0.50:5000',
                        'username': username,
                        'password': password,
                        'project_id': project.id,
                        'project_name': project_name,
                        'user_domain_name': 'Default',
                        'project_domain_name': 'Default',
                    },
                    'interface': 'public',
                    'identity_api_version': 3,
                    'region_name': location,
                }
            }
        }

        # Write the clouds.yaml file
        with open(clouds_yaml_path, 'w') as yaml_file:
            yaml.dump(clouds_yaml_content, yaml_file)

        # Store the project in memory (replace with persistent storage in production)
        user_projects[username] = {'project_id': project.id, 'project_name': project_name}
        user_instances[username] = []  # Initialize instances list for this user/project

        flash('Project created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('create_project.html')

@app.route('/projects/<username>/instances', methods=['GET'])
def list_instances(username):
    if username not in user_projects:
        flash('You need to create a project first.', 'warning')
        return redirect(url_for('create_project'))

    # Retrieve instances associated with this user's project from OpenStack
    instances = conn.compute.servers()
    instance_list = [{'name': instance.name, 'status': instance.status, 'id': instance.id} for instance in instances]
    
    return render_template('list_instances.html', instances=instance_list)

@app.route('/projects/<username>/create_instance', methods=['GET', 'POST'])
def create_instance(username):
    if username not in user_projects:
        flash('You need to create a project first.', 'warning')
        return redirect(url_for('create_project'))

    if request.method == 'POST':
        name = request.form['name']
        image_id = request.form['image']
        flavor_id = request.form['flavor']
        network_id = request.form['network']

        instance = conn.compute.create_server(
            name=name,
            image_id=image_id,
            flavor_id=flavor_id,
            networks=[{"uuid": network_id}]
        )
        
        instance = conn.compute.wait_for_server(instance)

        # Add instance information to user's instance list (for demonstration)
        user_instances[username].append({
            'name': instance.name,
            'status': instance.status,
            'id': instance.id
        })

        flash(f'Instance {instance.name} created successfully!', 'success')
        return redirect(url_for('list_instances', username=username))

    images = conn.compute.images()
    flavors = conn.compute.flavors()
    networks = conn.network.networks()
    
    return render_template('create_instance.html', images=images, flavors=flavors, networks=networks)

@app.route('/projects/<username>/instances/<instance_id>', methods=['DELETE'])
def delete_instance(username, instance_id):
    if username not in user_projects:
        flash('You need to create a project first.', 'warning')
        return redirect(url_for('create_project'))

    # Find and delete the instance from OpenStack
    try:
        conn.compute.delete_server(instance_id)
        
        # Remove from user's local list (for demonstration)
        user_instances[username] = [inst for inst in user_instances[username] if inst['id'] != instance_id]
        
        flash(f'Instance {instance_id} deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting instance: {str(e)}', 'danger')

    return redirect(url_for('list_instances', username=username))

@app.route('/projects/<username>/instances/<instance_id>/start', methods=['POST'])
def start_instance(username, instance_id):
    if username not in user_projects:
        flash('You need to create a project first.', 'warning')
        return redirect(url_for('create_project'))

    try:
        conn.compute.start_server(instance_id)
        
        flash(f'Instance {instance_id} started successfully!', 'success')
    except Exception as e:
        flash(f'Error starting instance: {str(e)}', 'danger')

    return redirect(url_for('list_instances', username=username))

@app.route('/projects/<username>/instances/<instance_id>/stop', methods=['POST'])
def stop_instance(username, instance_id):
    if username not in user_projects:
        flash('You need to create a project first.', 'warning')
        return redirect(url_for('create_project'))

    try:
        conn.compute.stop_server(instance_id)
        
        flash(f'Instance {instance_id} stopped successfully!', 'success')
    except Exception as e:
        flash(f'Error stopping instance: {str(e)}', 'danger')

    return redirect(url_for('list_instances', username=username))

@app.route('/projects/<username>/instances/<instance_id>/restart', methods=['POST'])
def restart_instance(username, instance_id):
    if username not in user_projects:
        flash('You need to create a project first.', 'warning')
        return redirect(url_for('create_project'))

    try:
        conn.compute.reboot_server(instance_id)
        
        flash(f'Instance {instance_id} restarted successfully!', 'success')
    except Exception as e:
        flash(f'Error restarting instance: {str(e)}', 'danger')

    return redirect(url_for('list_instances', username=username))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
