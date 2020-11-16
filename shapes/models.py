from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

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

# Example of a Song document
# {
#   "id":1,
#   "title":"St. Percy",
#   "artist_name":"Brockhampton",
#   "video_id":"rp-I-YGg6Hs"
# }

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    artist_name = db.Column(db.String)
    video_id = db.Column(db.String)

class SourceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Source
        include_relationships = True
        load_instance = True

class SongSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Song
        include_relationships = True
        load_instance = True
