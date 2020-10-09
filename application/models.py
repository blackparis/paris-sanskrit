from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)


class Aphorism(db.Model):
    __tablename__ = "aphorisms"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    topic = db.Column(db.String(100), nullable=False)
    subtopic = db.Column(db.String(100), nullable=True)
    rule = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.number}, {self.topic}, {self.subtopic}, {self.rule}"
