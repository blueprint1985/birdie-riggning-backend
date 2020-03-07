import re

from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow

def validatePhone(phone):
    regex = r"^((0046|\+46|0)7[02369])(((\s|\-)\d{3}\s\d{2}\s\d{2})|(\d{7})|(\d(\s|\-)\d{2}\s\d{2}\s\d{2})|(\-\d{7})|(\d\-\d{6}))$"
    result = re.search(regex, phone)

    if result == None:
        return False
    
    return True

class CrewSchema(Marshmallow().Schema):
    id = fields.Integer(dump_only=True)
    nickname = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True, validate=validatePhone)
    is_admin = fields.Boolean(missing=False)
