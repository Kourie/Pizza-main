
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
# over here we import flask for the website and sqlalchemy for the database
# import os to find files and paths

DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jess'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


db = SQLAlchemy(app)

# always refrence the file with capital P. this is done since moudles has a lowercase p
from Pizza import routes
from Pizza import models
# Pizza is the filename that we're in
