from run import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class CrewModel(db.Model):
    __tablename__ = 'crew'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nickname = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=0)
