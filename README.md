# Shapes Demo App

## Architecture

This is a simple framework for a single page javascript application that can be served completely 
as static files. The architecture is such that the entire application is encapsulated in as few 
files, none of whichhave any "moving parts" -- or server-side componenets, as possible.

However, there is also a server-side component -- an API that functions as a master SQLite file 
update process. This API *is* a "moving part" -- it updates the SQLite file. The entire SQLite 
file is refreshed on page load by the user.

The goal is to make a full featured web application that is also fully archivable as a small,
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
JSON payload failed validation. Missing key: id. Expected keys are: ('id', 'title', 'youtube_url', 'shape')
```

You should see the above message as a 400-status response when posting json with curl. The API is working.

