# creating database
'''
Students and books have one to many relationship
Student and registration model have one to many relationship
'''
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    borrowed_books = db.relationship('Book', backref='borrower', lazy=True)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)
    borrowed_by = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    due_date = db.Column(db.DateTime)
    due_amount = db.Column(db.Float, nullable=False)

class Registration(db.Model):
    __tablename__ = 'registration'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    registered_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    

    student = db.relationship('Student', backref=db.backref('registrations', lazy=True))
