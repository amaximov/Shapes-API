#Import required packages
from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import scoped_session, sessionmaker
from shapes.models import db, Source, Artist, Song, Shape, SourceSchema, ArtistSchema, SongSchema, ShapeSchema
from apispec import APISpec
import copy
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../www/shapes.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 

db.init_app(app)
app.app_context().push()
db.create_all()
mallow = Marshmallow(app)

# Create spec
spec = APISpec(
    title='Shapes API',
    version='1.0.0',
    info=dict(
        description='An API that describes some datatypes for support of the Shapes system'
    ),
    openapi_version="3.0.2",
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin()
    ]
)

spec.components.schema("Song", schema=SongSchema)

# Initialize schemas
song_schema = SongSchema()
songs_schema = SongSchema(many=True)

# Create a song
@app.route('/song', methods=['POST'])
def add_song():
    """Add Song view.
    ---
    post:
      summary: Create Song
      description: Post a single Song.
      responses:
        200:
          description: Song creation succeeded
          content:
            application/json:
              schema: SongSchema
        400:
          description: Creation failed. More details in error message.              
    """
    try:
        new_song = song_schema.load(request.json, session=db.session)
    except ValidationError as err:
        return err.messages, 400
    db.session.add(new_song)
    db.session.commit()
    return jsonify(song_schema.dump(new_song))

@app.route('/song', methods=['GET'])
def get_songs():
    """Get Songs.
    ---
    get:
      summary: List Songs
      description: Lists all songs
      responses:
        200:
          description: Song listing succeeded
          content:
            application/json:
              schema: SongSchema
    """
    songs = Song.query.all()
    return jsonify(songs_schema.dump(songs))

@app.route("/song/<int:song_id>", methods=['GET'])
def get_song(song_id):
    """Display Song
    ---
    get:
      summary: Display Song
      description: Display Song identified by <id>
      parameters:
        - name: song_id
          in: path
          description: Song ID
          type: integer
          required: true
      responses:
        200:
          description: Song update succeeded
          content:
            application/json:
              schema: SongSchema
        404:
          description: Song not found
    """
    try:
        song = Song.query.get(song_id)
    except Exception as e:
        return "Object not found for ID %s", 400
    return jsonify(song_schema.dump(song))

@app.route("/song/<int:song_id>", methods=['PUT'])
def update_song(song_id):
    """Update Song
    ---
    put:
      summary: Update Song
      description: Update Song identified by <id>
      parameters:
        - name: song_id
          in: path
          description: Song ID
          type: integer
          required: true
      responses:
        200:
          description: Song update succeeded
          content:
            application/json:
              schema: SongSchema
        400:
          description: Update failed. More details in error message.              
    """
    song = Song.query.get(song_id)
    try:
        updated_song = song_schema.load(request.json, instance=song)
    except ValidationError as err:
        return err.messages, 400
    db.session.commit()
    return jsonify(song_schema.dump(song))

@app.route("/song/<int:song_id>", methods=['DELETE'])
def delete_song(song_id):
    """Delete Song
    ---
    delete:
      summary: Delete Song
      description: Delete Song identified by <id>
      parameters:
        - name: song_id
          in: path
          description: Song ID
          type: integer
          required: true
      responses:
        200:
          description: Song delete succeeded
        400:
          description: Deletion failed. More details in error message.              
    """
    song = Song.query.get(song_id)
    db.session.delete(song)
    db.session.commit()
    return jsonify(song_schema.dump(song))

with app.test_request_context():
    spec.path(view=add_song)
    spec.path(view=delete_song)
    spec.path(view=get_song)
    spec.path(view=update_song)
    spec.path(view=get_songs)

with open('www/swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)
    
# this tricky little weirdness is python boilerplate for "if this file is executed directly, do [action]"
# where "action" here, is to call the "run" function on the flask "app" (in debug mode)
if __name__ == '__main__':
    app.run(debug=True)

