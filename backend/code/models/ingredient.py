import sqlite3
from db import db

class IngredientModel(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(80))
    name = db.Column(db.String(80))
    amount = db.Column(db.Integer)
    voltage = db.Column(db.Integer)
    pump = db.Column(db.Integer)

    def __init__(self, value, name, amount, voltage, pump):
        self.value = value
        self.name = name
        self.amount = amount
        self.voltage = voltage
        self.pump = pump

    def json(self):
        return {'id': self.id, 'value': self.value, 'name': self.name, 'amount': self.amount, 'voltage': self.voltage, 'pump': self.pump}

    @classmethod
    def find_by_value(cls, value):
        return cls.query.filter_by(value=value).first()
  
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_pump(cls, pump):
        return cls.query.filter_by(pump=pump).first()

    @classmethod
    def get_all_pumps(cls):
        return cls.query.filter(cls.pump != None).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()