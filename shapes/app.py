#Import required packages
from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import copy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../www/shapes.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 

db = SQLAlchemy(app)
mallow = Marshmallow(app)

class Song(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    youtube_id = db.Column(db.String)
    shape = db.Column(db.String)
    
    def __init__(self, title, youtube_id, shape):
        self.title = title
        self.youtube_id = youtube_id
        self.shape = shape
        
class SongSchema(mallow.Schema):    
    class Meta:
        fields = ('id','title','youtube_id','shape')

# Initialize schemas
song_schema = SongSchema()
songs_schema = SongSchema(many=True)

# Create a user
@app.route('/song', methods=['POST'])
def add_song():
    # use the "double star" operator to save some typing. Passes in the 
    # dictionary keys and values as arguments to the function (in this case, a constructor)
    try:
        song_schema.load(request.json)
    except mallow.ValidationError as err:
        return err.messages, 400
    new_song = Song(**request.json)
    db.session.add(new_song)
    db.session.commit()
    return song_schema.jsonify(new_song)

@app.route('/song', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    return jsonify(songs_schema.dump(songs))

@app.route("/song/<int:id>", methods=['PUT'])
def update_song(song_id):
    song = Song.query.get(song_id)
    try:
        updated_song = song_schema.load(request.json, instance=song)
    except mallow.ValidationError as err:
        return err.messages, 400
    db.session.commit()
    return song_schema.jsonify(song)

@app.route("/song/<int:id>", methods=['DELETE'])
def delete_song(song_id):
    song = Song.query.get(song_id)
    db.session.delete(song)
    db.session.commit()
    return song_schema.jsonify(song)


    


# this tricky little weirdness is python boilerplate for "if this file is executed directly, do [action]"
# where "action" here, is to call the "run" function on the flask "app" (in debug mode)
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

