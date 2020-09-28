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

# Example of a Source document
# {
# 	"_id" : ObjectId("5eb0e81665bca35b26437f21"),
# 	"parentEntity" : "Complex",
# 	"parentStream" : "Best New Music This Week",
# 	"instanceName" : "Brockhampton, Vince Staples, Lana Del Rey, and More",
# 	"publicationDate" : "2019-08-23T00:00:00-07:00",
# 	"location" : "https://www.complex.com/music/best-new-music-this-week-brockhampton-vince-staples-lana-del-rey"
# }

class Source(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_entity = db.Column(db.String)
    parent_stream = db.Column(db.String)
    instance_name = db.Column(db.String)
    publication_date = db.Column(db.DateTime)
    location = db.Column(db.String)

class Artist(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

class Shape(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

# Example of a Song document
# {
# 	"_id" : ObjectId("5eb0eb3d65bca35b26437f22"),
# 	"captureDate" : "2020-05-04T21:25:11-07:00",
# 	"captureSource" : ObjectId("5eb0e81665bca35b26437f21"),
# 	"songName" : "St. Percy",
# 	"artistName" : "Brockhampton",
# 	"videoId" : "rp-I-YGg6Hs"
# }

class Song(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    capture_date = db.Column(db.DateTime)
    capture_source = db.Column(db.Integer, foreign_key=Source)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    title = db.Column(db.String)
    video_id = db.Column(db.String)
    shape_id = db.Column(db.Integer, db.ForeignKey(Shape.id))

    artist = relationship('Artist', foreign_keys='Song.artist_id')
    shape = relationship('Shape', foreign_keys='Song.shape_id')
    
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

