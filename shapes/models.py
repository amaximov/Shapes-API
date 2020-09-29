from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Example of a Source document
# {
# 	"_id" : ObjectId("5eb0e81665bca35b26437f21"),
# 	"parentEntity" : "Complex",
# 	"parentStream" : "Best New Music This Week",
# 	"instanceName" : "Brockhampton, Vince Staples, Lana Del Rey, and More",
# 	"publicationDate" : "2019-08-23T00:00:00-07:00",
# 	"location" : "https://www.complex.com/music/best-new-music-this-week-brockhampton-vince-staples-lana-del-rey"
# }

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_entity = db.Column(db.String)
    parent_stream = db.Column(db.String)
    instance_name = db.Column(db.String)
    publication_date = db.Column(db.DateTime)
    location = db.Column(db.String)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

class Shape(db.Model):
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

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    capture_date = db.Column(db.DateTime)
    source_id = db.Column(db.Integer, db.ForeignKey(Source.id))
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    title = db.Column(db.String)
    video_id = db.Column(db.String)
    shape_id = db.Column(db.Integer, db.ForeignKey(Shape.id))

    artist = relationship('Artist', foreign_keys='Song.artist_id')
    shape = relationship('Shape', foreign_keys='Song.shape_id')
    capture = relationship('Source', foreign_keys='Song.source_id')
    
class SourceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Source
        include_relationships = True
        load_instance = True

class ArtistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
        include_relationships = True
        load_instance = True

class ShapeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Shape
        include_relationships = True
        load_instance = True

class SongSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Song
        include_relationships = True
        load_instance = True

