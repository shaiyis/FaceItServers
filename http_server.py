# in terminal:
# set FLASK_APP=http_server.py
# flask run
# write this to use pycharm with flask:
# if __name__ == '__main__':
#   app.run(debug=True)

# to see mongoDB state visually, just copy mongodb://localhost:27017/ to mongoDB Compass

from flask import Flask
from flask import request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)  # Flask app

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/todo_db")
db = mongodb_client.db

# mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/FaceIt")
# FaceIt_DB = mongodb_client.db

# print(FaceIt_DB.list_collection_names())


@app.route("/add_one")
def add_one():
    db.todos.insert_one({'title': "todo title", 'body': "todo body"})
    return jsonify(message="success")


@app.route("/add_many")
def add_many():
    db.todos.insert_many([
        {'_id': 1, 'title': "todo title one ", 'body': "todo body one "},
        {'_id': 2, 'title': "todo title two", 'body': "todo body two"},
        {'_id': 3, 'title': "todo title three", 'body': "todo body three"},
        {'_id': 4, 'title': "todo title four", 'body': "todo body four"},
        {'_id': 5, 'title': "todo title five", 'body': "todo body five"},
        {'_id': 6, 'title': "todo title six", 'body': "todo body six"},
        ])
    return jsonify(message="success")


@app.route("/login")
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    return "login " + username + " " + password


if __name__ == '__main__':
    app.run(debug=True)
