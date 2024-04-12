# SOP-Flashcards

This is a project that is made to help students learn faster.

source venv/bin/activate
flask --app main.py --debug run
flask --app main --debug run --port 5002

relationsship between user nad their cards 1:24:00

Known issues:
When creating new cards on the page editcards.html; they for some reason cannot be deleted, and if you reload the page they doubble. I do not know why this happens but when you go back to home, they will become like the others again.

When creating notes and reloading the page, the notes will doubble just like the new cards. why this happens i do not know, but it for sure has something to do with the way that the stack is treated, maybe they are not added into the stack that is being used?
