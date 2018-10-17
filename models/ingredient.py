import sqlite3
from db import db
from slugify import slugify

class IngredientModel(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    full_name = db.Column(db.String(80))
    amount = db.Column(db.Integer)
    voltage = db.Column(db.Integer)

    def __init__(self, full_name, amount, voltage):
        self.name = slugify(full_name)
        self.full_name = full_name
        self.amount = amount
        self.voltage = voltage

    def json(self):
        return {'id': self.id, 'name': self.name, 'full_name': self.full_name, 'amount': self.amount, 'voltage': self.voltage}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
  
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()