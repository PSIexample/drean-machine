import sqlite3
from db import db

class IngredientModel(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    amount = db.Column(db.Integer)

    def __init__(self,name,amount):
        self.name = name
        self.amount = amount

    def json(self):
        return {'name': self.name, 'amount': self.amount}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_ingredient(self):
        db.session.delete(self)
        db.session.commit()