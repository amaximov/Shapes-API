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

### index.html

### app.css

### app.js

### data.sqlite

### shapes

## Goals

The main goal of this application is to be as simple to understand and maintain, and as clean
and "manual-similar" as possble, meaning that it can be quickly be deconstructed by a novice
coder and understood (at least substantially) by simply following manual examples. I will
make a list of those sources from which I pulled instructions and documentation.

### Sources
 
https://tutorialwithproject.com/flask-rest-api-crud-operations/#define_and_initialize_marshmallow

Jagadananda Saint's tutorial on a simple Flask REST API that does "CRUD" (Create/Read/Update/Delete)



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



