import sqlite3
from db import db
from flask import json

class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(80))
    name = db.Column(db.String(80))

    def __init__(self, value, name):
        self.value = value
        self.name = name

    def json(self):
        return {'name': self.name}

    @classmethod
    def find_by_value(cls, value):
        recipe_name = cls.query.filter_by(value=value).first()
        return recipe_name

    @classmethod
    def find_by_id(cls, id):
        recipe_name = cls.query.filter_by(id=id).first()
        return recipe_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        return self.id

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()