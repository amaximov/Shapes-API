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
    validation_fields = copy.copy(SongSchema.Meta.fields)
    validation_fields = list(validation_fields)
    validation_fields.remove("id")
    # simple validation. compare each key in the schema with the keys we received in json post
    for key in validation_fields:
        if key not in request.json:
            return 'JSON payload failed validation. Missing key: %s. Expected keys are: %s\n' % (key, validation_fields), 400
    # simple validation. compare the length of the keys in the schema to the length of the
    # set of keys we received in json post.
    if len(validation_fields) != len(request.json):
        return "JSON payload faled validation. Too many keys. (extraneous data?) Expected keys are: %s\n" % (validation_fields,), 400

    # use the "double star" operator to save some typing. Passes in the 
    # dictionary keys and values as arguments to the function (in this case, a constructor)
    new_song = Song(**request.json)
    db.session.add(new_song)
    db.session.commit()
    return song_schema.jsonify(new_song)

# this tricky little weirdness is python boilerplate for "if this file is executed directly, do [action]"
# where "action" here, is to call the "run" function on the flask "app" (in debug mode)
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

