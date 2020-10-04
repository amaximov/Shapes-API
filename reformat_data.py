import json
from pprint import pprint
import re
from sqlalchemy import create_engine
from shapes.models import db, Source, Song, SourceSchema, SongSchema
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shapes.migrated.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 

db.init_app(app)
app.app_context().push()
db.create_all()
mallow = Marshmallow(app)

song_schema = SongSchema()
source_schema = SourceSchema()

source_mapping = {}

with open('data/sources.json', 'r') as sources:
    i = 0
    for line in sources.readlines():
        i += 1
        source = json.loads(line)
        source_mapping[source["_id"]["$oid"]] = i
        del(source["_id"])
        source["id"] = i
    
        new_source = source_schema.load(source, session=db.session)
        db.session.add(new_source)
        db.session.commit()

with open("data/songs.json", "r") as songs:
    i = 0
    for line in songs.readlines():
        i += 1
        song = json.loads(line)
        try:
            song["source"] = source_mapping.get(song["source_id"]["$oid"])
        except:
            song["source_id"] = None
        del(song["_id"])
        del(song["source_id"])
        song["id"] = i
        new_song = song_schema.load(song, session=db.session)
        db.session.add(new_song)
        db.session.commit()
