import sqlite3
from db import db

class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    timestamp = db.Column(db.String(80))

    user = db.relationship('UserModel')
    recipe = db.relationship('RecipeModel')

    def __init__(self,user_id,recipe_id,timestamp):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.timestamp = timestamp

    def json(self):
        return {'user_id': self.user_id, "recipe_id": self.recipe_id, "timestamp": self.timestamp}

    @classmethod
    def find_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_recipe(cls, recipe_id):
        return cls.query.filter_by(recipe_id=recipe_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()