from flask import Blueprint

signin = Blueprint('signin', __name__)

from signin import routes