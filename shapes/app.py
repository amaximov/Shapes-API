#Import required packages
from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import scoped_session, sessionmaker
from shapes.models import db, Source, Artist, Song, Shape, SourceSchema, ArtistSchema, SongSchema, ShapeSchema
import copy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../www/shapes.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 

db.init_app(app)
app.app_context().push()
db.create_all()
mallow = Marshmallow(app)

# Initialize schemas
song_schema = SongSchema()
songs_schema = SongSchema(many=True)

# Create a song
@app.route('/song', methods=['POST'])
def add_song():
    try:
        new_song = song_schema.load(request.json, session=db.session)
    except ValidationError as err:
        return err.messages, 400
    db.session.add(new_song)
    db.session.commit()
    return jsonify(song_schema.dump(new_song))

@app.route('/song', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    return jsonify(songs_schema.dump(songs))

@app.route("/song/<int:id>", methods=['PUT'])
def update_song(song_id):
    song = Song.query.get(song_id)
    try:
        updated_song = song_schema.load(request.json, instance=song)
    except ValidationError as err:
        return err.messages, 400
    db.session.commit()
    return jsonify(song_schema.dumps(song))

@app.route("/song/<int:id>", methods=['DELETE'])
def delete_song(song_id):
    song = Song.query.get(song_id)
    db.session.delete(song)
    db.session.commit()
    return jsonify(song_schema.dumps(song))

# this tricky little weirdness is python boilerplate for "if this file is executed directly, do [action]"
# where "action" here, is to call the "run" function on the flask "app" (in debug mode)
if __name__ == '__main__':
    app.run(debug=True)

