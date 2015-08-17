# flask
from flask import Blueprint

auth = Blueprint('auth', __name__)

# local
from . import views
