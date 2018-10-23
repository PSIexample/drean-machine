import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    current_order = db.Column(db.String(80))
    rfid = db.Column(db.String(80))

    def __init__(self, username, password, current_order):
        self.username = username
        self.password = password
        self.current_order = current_order
        self.rfid = "1234"

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_rfid(cls, rfid):
        return cls.query.filter_by(rfid=rfid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()