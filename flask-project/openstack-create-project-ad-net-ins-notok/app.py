from flask import Flask, render_template, request, redirect, url_for, flash, session
from openstack import connection
from openstack.exceptions import ConflictException, NotFoundException
from flask import send_file
import sqlite3
import os
import paramiko
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Flask-এর জন্য সিক্রেট কী

# ডাটাবেস ফাইল পাথ
DATABASE = 'openstack_projects.db'

# ডাটাবেস সংযোগ তৈরি
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ডাটাবেস টেবিল তৈরি
def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

# OpenStack সংযোগ তৈরি
def create_connection():
    return connection.Connection(cloud='openstack')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        username = request.form['username']
        password = request.form['password']

        try:
            conn = create_connection()

            # নতুন প্রজেক্ট তৈরি
            project = conn.identity.create_project(name=project_name)

            # নতুন ইউজার তৈরি
            user = conn.identity.create_user(name=username, password=password)

            # ইউজারের প্রাইমারি প্রজেক্ট সেট করুন
            conn.identity.update_user(user.id, default_project_id=project.id)

            # রোল খুঁজুন বা তৈরি করুন
            role_name = "member"
            role = conn.identity.find_role(role_name)
            if not role:
                role = conn.identity.create_role(name=role_name)

            # ইউজারকে প্রজেক্টে অ্যাড করুন
            conn.identity.assign_project_role_to_user(project.id, user.id, role.id)

            # অ্যাডমিন ইউজারকে প্রজেক্টের অ্যাডমিন হিসেবে যুক্ত করুন
            admin_user = conn.identity.find_user('admin')
            admin_role = conn.identity.find_role('admin')
            if admin_user and admin_role:
                conn.identity.assign_project_role_to_user(project.id, admin_user.id, admin_role.id)
            else:
                flash("অ্যাডমিন ইউজার বা রোল খুঁজে পাওয়া যায়নি!", 'error')
                try:
                    # প্রাইভেট নেটওয়ার্ক তৈরি করুন
                    network_name = f"{project_name}-private"
                    network = conn.network.create_network(name=network_name, project_id=project.id)

                    # সাবনেট তৈরি করুন
                    subnet_name = f"{project_name}-subnet"
                    subnet = conn.network.create_subnet(
                        name=subnet_name,
                        network_id=network.id,
                        ip_version=4,
                        cidr='10.0.0.0/24',
                        gateway_ip='10.0.0.1'
                    )
                except Exception as e:
                    flash(f"নেটওয়ার্ক তৈরি করতে ত্রুটি হয়েছে: {str(e)}", 'error')


            # ডাটাবেসে প্রজেক্ট এবং ইউজার তথ্য সংরক্ষণ
            db_conn = get_db_connection()
            db_conn.execute('INSERT INTO projects (project_id, project_name, username, password) VALUES (?, ?, ?, ?)',
                            (project.id, project.name, username, password))
            db_conn.commit()
            db_conn.close()

            # সেশনে প্রজেক্ট এবং ইউজার তথ্য সংরক্ষণ
            session['project_id'] = project.id
            session['project_name'] = project.name
            session['username'] = username
            session['password'] = password

            flash(f"প্রজেক্ট '{project_name}' এবং ইউজার '{username}' সফলভাবে তৈরি হয়েছে!", 'success')
            return redirect(url_for('manage_project'))

        except ConflictException:
            flash(f"প্রজেক্ট বা ইউজার ইতিমধ্যেই বিদ্যমান!", 'error')
        except NotFoundException:
            flash(f"রোল বা অন্যান্য রিসোর্স খুঁজে পাওয়া যায়নি!", 'error')
        except Exception as e:
            flash(f"একটি ত্রুটি ঘটেছে: {str(e)}", 'error')

    return render_template('create_project.html')

@app.route('/manage_project', methods=['GET', 'POST'])
def manage_project():
    if 'project_id' not in session:
        flash("প্রথমে একটি প্রজেক্ট তৈরি করুন!", 'error')
        return redirect(url_for('home'))

    project_id = session['project_id']
    username = session['username']
    password = session['password']

@app.route('/download_key/<key_name>')
def download_key(key_name):
    return send_file(f"{key_name}.pem", as_attachment=True)

    # প্রজেক্টের জন্য OpenStack সংযোগ তৈরি
    conn = connection.Connection(
        auth_url='http://192.168.0.50:5000/v3',
        project_id=project_id,
        username=username,
        password=password,
        user_domain_name='Default',
        project_domain_name='Default'
    )

    if request.method == 'POST':
        action = request.form.get('action')
        instance_id = request.form.get('instance_id')

        if action == 'create_instance':
            instance_name = request.form['instance_name']
            image_id = request.form['image_id']
            flavor_id = request.form['flavor_id']

            # প্রাইভেট নেটওয়ার্ক এবং পাবলিক নেটওয়ার্ক খুঁজুন
            private_network_name = f"{session['project_name']}-private"
            private_network = conn.network.find_network(private_network_name)
            public_network = conn.network.find_network('public')

            # নতুন SSH কী তৈরি করুন
            key_name = f"{instance_name}-key"
            key = conn.compute.create_keypair(name=key_name)
            with open(f"{key_name}.pem", 'w') as f:
                f.write(key.private_key)

            # ইনস্ট্যান্স তৈরি করুন
            instance = conn.compute.create_server(
                name=instance_name,
                image_id=image_id,
                flavor_id=flavor_id,
                networks=[{'uuid': private_network.id}, {'uuid': public_network.id}],
                key_name=key_name
            )

            flash(f"ইনস্ট্যান্স '{instance_name}' সফলভাবে তৈরি হয়েছে!", 'success')
            return render_template('download_key.html', key_name=key_name)

        elif action == 'delete_instance':
            conn.compute.delete_server(instance_id)
            flash(f"ইনস্ট্যান্স ডিলিট করা হয়েছে!", 'success')

        elif action == 'start_instance':
            conn.compute.start_server(instance_id)
            flash(f"ইনস্ট্যান্স স্টার্ট করা হয়েছে!", 'success')

        elif action == 'stop_instance':
            conn.compute.stop_server(instance_id)
            flash(f"ইনস্ট্যান্স স্টপ করা হয়েছে!", 'success')

    # প্রজেক্টের আন্ডারে সকল ইনস্ট্যান্স লিস্ট ভিউ
    instances = list(conn.compute.servers())
    return render_template('manage_project.html', instances=instances)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
