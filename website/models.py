from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class FlashcardStack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  
    flashcards = db.relationship("Flashcard", backref="stack", lazy=True) 

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000), nullable=False)  
    answer = db.Column(db.String(1000), nullable=False) 
    stack_id = db.Column(db.Integer, db.ForeignKey("flashcard_stack.id"), nullable=False)  


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship("Note")
    flashcard_stacks = db.relationship("FlashcardStack", backref="user", lazy=True) 

