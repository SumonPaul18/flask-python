from flask import Flask, redirect, url_for, flash, render_template, request
from flask_login import (
    LoginManager, UserMixin, current_user,
    login_required, login_user, logout_user
)
from main import app, db
from models import User, Project

@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        description = request.form.get('description')
        instance_type = request.form.get('instance_type')
        image = request.form.get('image')
        network = request.form.get('network')

        # Create a new project instance
        new_project = Project(
            name=project_name,
            description=description,
            instance_type=instance_type,
            image=image,
            network=network,
            user_id=current_user.id
        )

        # Add the new project to the database
        db.session.add(new_project)
        db.session.commit()

        flash(f'Project "{project_name}" created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_project.html')