#Import required packages
from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shapes.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 

db = SQLAlchemy(app)
mallow = Marshmallow(app)

class Song(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    youtube_url = db.Column(db.String)
    shape = db.Column(db.String)
    
    def __init__(self, title, youtube_url, shape):
        self.title = title
        self.youtube_url = youtube_url
        self.shape = shape

class SongSchema(mallow.Schema):
    class Meta:
        fields = ('id','title','youtube_url','shape')

# Initialize schemas
song_schema = SongSchema()
songs_schema = SongSchema(many=True)
