from flask import Blueprint

signin = Blueprint('signin',__name__,template_folder='templates')

from signin import routes