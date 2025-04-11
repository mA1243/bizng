from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    last_login = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    phoneno = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    img = db.Column(db.String(200))
    website = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now, nullable=False)
    
    state_id = db.Column(db.Integer, db.ForeignKey('state.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    lga_id = db.Column(db.Integer, db.ForeignKey('lga.id', ondelete='CASCADE'), nullable=False)
    
    state = db.relationship('State', backref=db.backref('businesses', lazy=True, cascade="all, delete"))
    category = db.relationship('Category', backref=db.backref('businesses', lazy=True, cascade="all, delete"))
    owner = db.relationship('User', backref=db.backref('businesses', lazy=True, cascade="all, delete"))
    lga = db.relationship('LGA', backref=db.backref('businesses', lazy=True, cascade="all, delete"))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    date_reviewed = db.Column(db.DateTime, default=datetime.now, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id', ondelete='CASCADE'), nullable=False)

    business = db.relationship('Business', backref=db.backref('reviews', lazy=True, cascade="all, delete"))

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    dp = db.Column(db.String(200))
    date_registered = db.Column(db.DateTime, default=datetime.now, nullable=False)

class LGA(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id', ondelete='CASCADE'), nullable=False)

    state = db.relationship('State', backref=db.backref('lgas', lazy=True, cascade="all, delete"))
    
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_type = db.Column(db.String(50), nullable=False)  # 'business' or 'review'
    report_reason = db.Column(db.String(255), nullable=False)
    report_details = db.Column(db.Text, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id', ondelete='CASCADE'), nullable=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id', ondelete='CASCADE'), nullable=True)
    date_reported = db.Column(db.DateTime, default=datetime.now, nullable=False)

    business = db.relationship('Business', backref=db.backref('reports', lazy=True, cascade="all, delete"))
    review = db.relationship('Review', backref=db.backref('reports', lazy=True, cascade="all, delete"))