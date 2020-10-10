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


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    subtopics = db.relationship("SubTopic", backref='topic', lazy=True)


class SubTopic(db.Model):
    __tablename__ = "subtopics"
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rules = db.relationship("Aphorism", backref='subtopic', lazy=True)


class Aphorism(db.Model):
    __tablename__ = "aphorisms"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    subtopic_id = db.Column(db.Integer, db.ForeignKey("subtopics.id"), nullable=False)
    rule = db.Column(db.Text, nullable=False)