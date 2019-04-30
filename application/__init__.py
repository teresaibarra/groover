"""
initializes groover using the Flask library.

"""
import os
from flask import Flask
from application import routes

APP = Flask(__name__)
SECRET_KEY = os.urandom(32)
APP.config['SECRET_KEY'] = SECRET_KEY
