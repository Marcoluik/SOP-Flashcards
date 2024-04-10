from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .models import Note, Flashcard, FlashcardStack
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note has been created!!", category="success")
    return render_template("home.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note has been deleted", category="success")
            
    return jsonify({})
    
@views.route("/flashcards", methods=["GET", "POST"])
@login_required
def flashcards():
    return render_template("flashcards.html", user=current_user)

@views.route("/createflashcards", methods=["GET", "POST"])
@login_required
def createflashcards():
    if request.method == "POST":
        stack_name = request.form.get("stack_name")
        question = request.form.get("question")
        answer = request.form.get("answer")

        stack = FlashcardStack.query.filter_by(title=stack_name, user_id=current_user.id).first()

        if not stack:
            new_stack = FlashcardStack(title=stack_name, user_id=current_user.id)
            db.session.add(new_stack)
            db.session.commit()
            flash("New flashcard stack created", category="success")
            stack = new_stack
            
        new_flashcard = Flashcard(question=question, answer=answer, stack_id=stack.id)
        db.session.add(new_flashcard)
        db.session.commit()
        flash("New flashcard has been added", category="success")



    return render_template("createflashcards.html", user=current_user)

