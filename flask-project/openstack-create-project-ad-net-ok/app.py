from flask import Flask, render_template, request, redirect, url_for, flash, session
from openstack import connection
from openstack.exceptions import ConflictException, NotFoundException
import sqlite3
import os

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

            # প্রাইভেট নেটওয়ার্ক তৈরি করুন
            try:
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
                flash(f"নেটওয়ার্ক '{network_name}' এবং সাবনেট '{subnet_name}' সফলভাবে তৈরি হয়েছে!", 'success')
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
            return redirect(url_for('view_resources'))

        except ConflictException:
            flash(f"প্রজেক্ট বা ইউজার ইতিমধ্যেই বিদ্যমান!", 'error')
        except NotFoundException:
            flash(f"রোল বা অন্যান্য রিসোর্স খুঁজে পাওয়া যায়নি!", 'error')
        except Exception as e:
            flash(f"একটি ত্রুটি ঘটেছে: {str(e)}", 'error')

    return render_template('create_project.html')

@app.route('/view_resources')
def view_resources():
    if 'project_id' not in session:
        flash("প্রথমে একটি প্রজেক্ট তৈরি করুন!", 'error')
        return redirect(url_for('home'))

    project_id = session['project_id']
    username = session['username']
    password = session['password']

    # প্রজেক্টের জন্য OpenStack সংযোগ তৈরি
    conn = connection.Connection(
        auth_url='http://192.168.0.50:5000/v3',
        project_id=project_id,
        username=username,
        password=password,
        user_domain_name='Default',
        project_domain_name='Default'
    )

    # ইনস্ট্যান্স লিস্ট
    instances = list(conn.compute.servers())

    # নেটওয়ার্ক লিস্ট
    networks = list(conn.network.networks())

    # ইমেজ লিস্ট
    images = list(conn.compute.images())

    # ফ্লেভার লিস্ট
    flavors = list(conn.compute.flavors())

    # কী লিস্ট
    keys = list(conn.compute.keypairs())

    return render_template('view_resources.html', instances=instances, networks=networks, images=images, flavors=flavors, keys=keys)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)