from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class CrewSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nickname = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    is_admin = fields.Boolean()
