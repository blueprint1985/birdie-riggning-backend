import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "mysql://root:dinpappa@localhost:3306/birdierigg"