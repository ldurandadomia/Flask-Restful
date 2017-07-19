from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Declaration de l'application Flask
app = Flask(__name__)

# Declaration du modele de donnees
app.config.from_object('config_auth')
db = SQLAlchemy(app)

from authapp import models
from authapp.view_errorhandler import MyApi

# Declaration des APIs
api = MyApi(app)

from authapp import view_objects
from authapp import view_single_object
from authapp import view_def_rules
from authapp import view_single_def_rule
from authapp import view_auth_rules
from authapp import view_single_auth_rule
