#Import required packages
from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shapes.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 

db = SQLAlchemy(app)
mallow = Marshmallow(app)
