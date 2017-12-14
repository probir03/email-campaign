# from __init__ import app

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('env.py')

db = SQLAlchemy(app)
app.config['broker_url'] = 'redis://localhost:6379/0'



	