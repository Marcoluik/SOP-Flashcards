# This application is taken from
# https://www.geeksforgeeks.org/flask-creating-first-simple-application/

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World"


if __name__ == "__main__":
    app.run()
