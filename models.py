from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    observations = db.relationship("Observation", backref="city", lazy=True, cascade="all, delete-orphan")

class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"), nullable=False)
    week_label = db.Column(db.String(32), nullable=False)  # e.g., 'Wk 40'
    cases = db.Column(db.Integer, nullable=False, default=0)

class Indicator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"), nullable=False)
    rt = db.Column(db.Float, nullable=True)  # transmission rate
    r0 = db.Column(db.Float, nullable=True)  # basic reproduction number
    hospitalization_rate = db.Column(db.Float, nullable=True)  # percentage
    computed_at = db.Column(db.DateTime, default=datetime.utcnow)
