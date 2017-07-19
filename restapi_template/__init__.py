from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask application instantiation
app = Flask(__name__)

# Flask environment variable initialisation
app.config.from_object('config')

# Database instantiation
db = SQLAlchemy(app)

# Data model instantiation
from restapp import models

# REST error management
from restapp.view_errorhandler_v3 import MyApi

# REST APIs instantiation
api = MyApi(app)

# Other sub-modules import 
from <module> import <sub-module> 
...
