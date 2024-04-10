# This application is taken from
# https://www.geeksforgeeks.org/flask-creating-first-simple-application/
# This is the second example. Try it out on. http://127.0.0:5000/hello/Marco
from flask import Flask

app = Flask(__name__)


@app.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}! This is working!"


if __name__ == "__main__":
    app.run()
