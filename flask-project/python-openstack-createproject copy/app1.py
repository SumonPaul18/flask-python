import os
import uuid
import yaml  # Ensure PyYAML is installed: pip install pyyaml
from flask import Flask, jsonify, request, render_template
from openstack import connection

app = Flask(__name__)

# Establish OpenStack connection
conn = connection.Connection(cloud='mycloud')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/instances', methods=['GET'])
def list_instances():
    instances = conn.compute.servers()
    instance_list = [{'name': instance.name, 'status': instance.status} for instance in instances]
    return render_template('list_instances.html', instances=instance_list)


@app.route('/instances/<instance_id>', methods=['GET'])
def get_instance(instance_id):
    instance = conn.compute.get_server(instance_id)
    if instance:
        instance_info = {'name': instance.name, 'status': instance.status, 'id': instance.id}
        return jsonify(instance_info)
    else:
        return jsonify({'error': 'Instance not found'}), 404


@app.route('/create_instance', methods=['GET', 'POST'])
def create_instance():
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
        return jsonify({'name': instance.name, 'status': instance.status, 'id': instance.id})

    images = conn.compute.images()
    flavors = conn.compute.flavors()
    networks = conn.network.networks()
    return render_template('create_instance.html', images=images, flavors=flavors, networks=networks)


@app.route('/instances/<instance_id>', methods=['DELETE'])
def delete_instance(instance_id):
    instance = conn.compute.get_server(instance_id)
    if instance:
        conn.compute.delete_server(instance)
        return jsonify({'status': 'Instance deleted'})
    else:
        return jsonify({'error': 'Instance not found'}), 404


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
                        'auth_url': 'https://your-auth-url.com/v3',
                        'username': username,
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

        # Write the clouds.yaml file
        with open(clouds_yaml_path, 'w') as yaml_file:
            yaml.dump(clouds_yaml_content, yaml_file)

        return jsonify({'status': 'Project created', 'clouds_yaml_file': unique_filename})

    return render_template('create_project.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
