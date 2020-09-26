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

# Create a user
@app.route('/song', methods=['POST'])
def add_song():
    # simple validation. compare each key in the schema with the keys we received in json post
    for key in SongSchema.Meta.fields:
        if key not in request.json:
            raise Exception('JSON payload failed validation. Missing key: %s' % key)
    # simple validation. compare the length of the keys in the schema to the length of the
    # set of keys we received in json post.
    if len(SongSchema.Meta.fields) != len(request.json):
        raise Exception("JSON payload faled validation. Too many keys. (extraneous data?)")

    # use the "double star" operator to save some typing. Passes in the 
    # dictionary keys and values as arguments to the function (in this case, a constructor)
    new_song = Song(**request.json)
    db.session.add(new_song)
    db.session.commit()
    return song_schema.jsonify(new_song)
