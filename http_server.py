from flask import Flask

app = Flask(__name__)  # Flask app


@app.route("/")
def hello():
    return "Hello World!"
