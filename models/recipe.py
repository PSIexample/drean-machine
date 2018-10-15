import sqlite3
from db import db
from models.mixing import MixingModel
from flask import json

class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    #items = db.relationship('MixingModel', lazy='dynamic')

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'name': self.name}

    @classmethod
    def find_by_name(cls, name):
        recipe_name = cls.query.filter_by(name=name).first()
        ingredients = MixingModel.find_by_recipe(recipe_name.id)
 
        return recipe_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        return self.id

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()