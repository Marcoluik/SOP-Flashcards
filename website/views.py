from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
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

@views.route("/editcards", methods=["GET", "POST"])
@login_required
def editcards():
    stackId = request.args.get('stackId', None)  

    if not stackId:
        flash('No stack ID provided.', category='error')
        return redirect(url_for('views.home'))
    
    stack = FlashcardStack.query.get(stackId)
    if not stack:
        flash('Stack not found.', 'error')
        return redirect(url_for('views.home')) 

    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")

        if question and answer:  
            new_flashcard = Flashcard(question=question, answer=answer, stack_id=stack.id)
            db.session.add(new_flashcard)
            db.session.commit()
            flash("New flashcard has been added", category="success")
        else:
            flash("Question and answer cannot be empty.", category="error")
         
    return render_template("editcards.html", user=current_user, stack=stack)

@views.route("/update_flashcard/<int:flashcard_id>", methods=["POST"])
@login_required
def update_flashcard(flashcard_id):
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    
    if flashcard.stack.user_id != current_user.id:
        flash("Unauthorized to update this flashcard.", "error")
        return redirect(url_for('views.editcards', stackId=flashcard.stack_id))

    question = request.form.get("question").strip()
    answer = request.form.get("answer").strip()
    
    if question and answer:
        flashcard.question = question
        flashcard.answer = answer
        db.session.commit()
        flash("Flashcard updated successfully!", "success")
    else:
        flash("Both question and answer are required.", "error")
    
    return redirect(url_for('views.editcards', stackId=flashcard.stack_id))

@views.route("/delete-card", methods=["POST"])
def deleteflashcard():
    data = json.loads(request.data)
    cardId = data["cardId"]
    card = Flashcard.query.get(cardId)
    if card:
        stack = FlashcardStack.query.get(card.stack_id)
        if stack and stack.user_id == current_user.id:
            db.session.delete(card)
            db.session.commit()
            return jsonify({"success": True, "message": "Card has been deleted"})
        else:
            return jsonify({"error": "Unauthorized"}), 403
    else:
        return jsonify({"error": "Card not found"}), 404


@views.route("/train", methods=["GET", "POST"])
@login_required
def training():
    stackId = request.args.get('stackId', None)  

    if stackId is None:
    
        flash('No stack ID provided.', category='error')
        return redirect(url_for('views.home'))
    else:
        stack = FlashcardStack.query.get(stackId)
    
    if not stack:
        flash('Stack not found.', 'error')
        return redirect(url_for('views.home')) 
    


    if request.method == "POST":
        pass
         

    return render_template("train.html", user=current_user, stack=stack)
