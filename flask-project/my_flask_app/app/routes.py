from flask import Blueprint, render_template, request, redirect, url_for
from app.models import FormData
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/submit', methods=['POST'])
def submit():
    field_name = request.form.get('field_name')
    field_value = request.form.get('field_value')
    field_description = request.form.get('field_description')
    
    new_data = FormData(field_name=field_name, field_value=field_value, field_description=field_description)
    db.session.add(new_data)
    db.session.commit()
    
    return redirect(url_for('main.index'))