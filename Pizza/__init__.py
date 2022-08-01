from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path

DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jess'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


db = SQLAlchemy(app)

#always refrence the file with capital P. this is done since modles has a lowercase p
from Pizza import models
from Pizza import routes



    