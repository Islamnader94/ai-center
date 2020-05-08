from flask import Flask
from marshmallow import Schema, fields, pre_load, validate, ValidationError
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class DataScanned(db.Model):
    __tablename__ = 'scaned_data'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone =  db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, email, phone):
        self.email = email
        self.phone = phone

class DataScannedSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True)
    phone =fields.String(required=True)