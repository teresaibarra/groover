"""
initializes groover using the Flask library.

"""
import os
from flask import Flask

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True

from application import routes
