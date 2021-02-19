# Shapes Demo App

## Architecture

This is a simple framework for a single page javascript application that can be served completely 
as static files. The architecture is such that the entire application is encapsulated in as few 
files as possible, none of which have any "moving parts" -- or server-side componenets.

However, there is a separate server-side component -- an API that functions as a master SQLite file 
update process. This API *is* a "moving part" -- it *writes* to the SQLite file. The entire SQLite 
file is downloaded on page load by the user.

The goal is to make a full-featured web application that is also fully archivable as a small,
clear set of static files, so that a point-in-time snapshot is always a complete version of the
application.

## The Files

### www

the directory that contains all files that should be available to the public internet

### www/index.html

the html file that bootstraps the shapes application

### www/app.css

CSS that styles the shapes application

### www/app.js

the javascript code that renders and runs the shapes application

### www/shapes.sqlite

the sqlite data file that is used by the API for _writing_ and by the html/javascript file for _reading_

### shapes

the directory containing python application files (a python "module").

### conf

the directory containing apache24 configuration file

## Goals

The main goal of this application is to be as simple to understand and maintain, and as clean
and "manual-similar" as possble, meaning that it can be quickly be deconstructed by a novice
coder and understood (at least substantially) by simply following manual examples. I will
make a list of those sources from which I pulled instructions and documentation.

### Sources
 
https://tutorialwithproject.com/flask-rest-api-crud-operations/#define_and_initialize_marshmallow

Jagadananda Saint's tutorial on a simple Flask REST API that does "CRUD" (Create/Read/Update/Delete)

https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/

The flask tutorial on how to set up your app initially

https://github.com/sql-js/sql.js

SQL.js documentation. in particular: https://github.com/sql-js/sql.js/wiki/Load-a-database-from-the-server

https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation
Marshmallow Schema documentation. I suspected this did validation for you, and added boilerplate
from this so we didn't have to "repeat ourselves." (https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

We'll make more progress towards DRY as the code matures.

https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
documentation on how to set up foreign key relationships for SQLAlchemy (via flask-sqlalchemy,
a bridge library). The answer to this question has many good points that the CRUD tutorial's code
overlooked.

https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
documentation on how to move models into a separate file. Keeping all of the data modeling
in the same place as the URL routing etc is confusing and bad form.

https://dev.to/djiit/documenting-your-flask-powered-api-like-a-boss-9eo
tutorial on how to make your flask API (such as ours) "self-documenting"

## Technology Choices

### API Packages (python side)

#### Python
chosen for simplicity of syntax and relative maintainability. Python has many stable
packages and libraries and is a good choice for a novice coding language, but is also a real
programming tool (not a toy)

#### Flask
chosen again for simplicity. This is a relatively lightweight (but mature) python web
application framework.

#### SQLAlchemy
an "Object-Relational Model" (ORM) framework that's "the default" for use with 
Flask, particularly as wrapped by Marshmallow. Object relational models are not
strictly necessary in this case, but it's nice to have them when building a JSON
API. They also provide a clear, declarative model of your data -- which is a very
useful thing to conceptualize your problem.

#### Marshmallow
Marshmallow is a library that provides "serialization" -- or the ability to transform
an in-memory object into a string, and vice versa. (A "string" is a set of characters,
stored in order, usually terminated by a null byte. This differs from how an object
is stored in memory -- usually as some kind of representation of the data types
stored in its constituent fields. Transforming data between these two representations
is rather complex and is the object of "serialization" [memory-to-string] and "deserialization"
[string-to-memory]. It's called "serialization" because the bits/bytes of a string are 
transmitted in "series")

#### apispec
Makes a "self-documenting" API -- producing a swagger.json which will be consumed
by redoc to make a nice UI that documents how the API works (see below).

### Data storage

#### SQLite
chosen because it's SQLite. A magnificently portable SQL engine that (importantly)
creates a single flat-file representation of your data. This is ideal for versioning, 
backup, and easy synchronization (you just copy the file in all three cases).

I have used SQLite in many unusual contexts over time, and it has proven itself as a 
relatively quick and very reliable tool.

### Client Side

#### SQL.js
allows you to access a sqlite database (directly) in the browser

#### ReDoc (https://github.com/Redocly/redoc)
small, portable UI to transform swagger.json into a usable UI with example documents
for the various API endpoints. One of the hard things about APIs is "What data am I 
supposed to send?"

### Starting the Server

These are "simple" instructions on setting up a python "virtual environment" -- a small
virtualized installation of python that's local to your current project. This represents
a special, discardable (deletable) way to test out libraries for your project that don't
get installed globally (so annoying!). It's a good practice to use virtual environments
so you can easily reproduce the python environment from machine to machine.

Python comes with a package manager called "pip" (it doesn't quite "come with" it but
it's the usual default). Pip is used to install packages from a repo called pypi (https://pypi.org).
Pip and Pypi are nice, stable places where code kind of lives to be installed as a library.

If you've never used your python environment before, you should install virtualenv globally before
you begin, and install pip globally (because it should really be global).

```
sudo easy_install pip
sudo pip install virtualenv
```

Now make a virtual environment.

```
virtualenv -p python3 venv
```

Now activate your virtual environment. This is something you'll need to do each time to get
your server running.

```
source venv/bin/activate
```

Your prompt should change now, indicating that you're "in" a virtualenv. This means that you're
using a python binary that's local to the virtual environment, along with a set of libraries that's
installed below the `venv` directory. If you make a mistake you can always delete and re-initialize
the virtual environment.

Next, install libraries from the "requirements.txt" file.

```
pip install -r requirements.txt
```

Now start the flask app

```
python shapes/app.py
```

Now make the first request:

```
$ curl -d '{"hello":"world"}' -H 'content-type: application/json' localhost:5000/song
JSON payload failed validation. Missing key: title. Expected keys are: ('title', 'youtube_url', 'shape')
```

You should see the above message as a 400-status response when posting json with curl. The API is working.

## Docker

### Local developer setup

#### Overview

Docker'izing development environment ensures that Python setup can run anywhere regardless of Operating System 
or local Python setup.

There are two parts to the setup - the Docker image itself (`Dockerfile` - Linux OS, Python language runtime, 
our dependencies and source code, and the command to start it all up),
and the development setup (`docker-compose.yml`) where we mount our local code directory 
(which includes the sqlite database data) into the container, so that we can live edit our 
source code, and the Flask app running in the container could notice the changes and reload itself 
(since it is running in debug mode).

In development mode, Docker pulls a linux distro with latest of Python 3 installed, 
then installs dependencies for the API. 

* install both `docker` and `docker-compose`
* run `docker-compose up` - it will build the containers if needed, and then run the app and follow the logs
* test it as usual using the `curl` command above