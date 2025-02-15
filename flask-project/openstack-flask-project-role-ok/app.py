from flask import Flask, render_template, request, redirect, url_for, flash
from openstack import connection
from openstack.exceptions import ConflictException, NotFoundException

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Flask-এর জন্য সিক্রেট কী

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
            role_name = "member"  # অথবা আপনার নির্ধারিত রোলের নাম
            role = conn.identity.find_role(role_name)
            if not role:
                role = conn.identity.create_role(name=role_name)

            # ইউজারকে প্রজেক্টে অ্যাড করুন
            conn.identity.assign_project_role_to_user(project.id, user.id, role.id)

            flash(f"প্রজেক্ট '{project_name}' এবং ইউজার '{username}' সফলভাবে তৈরি হয়েছে!", 'success')
            return redirect(url_for('home'))

        except ConflictException:
            flash(f"প্রজেক্ট বা ইউজার ইতিমধ্যেই বিদ্যমান!", 'error')
        except NotFoundException:
            flash(f"রোল বা অন্যান্য রিসোর্স খুঁজে পাওয়া যায়নি!", 'error')
        except Exception as e:
            flash(f"একটি ত্রুটি ঘটেছে: {str(e)}", 'error')

    return render_template('create_project.html')

if __name__ == '__main__':
    app.run(debug=True)