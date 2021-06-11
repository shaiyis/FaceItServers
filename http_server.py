# in terminal:
# set FLASK_APP=http_server.py
# flask run
# write this to use pycharm with flask:
# if __name__ == '__main__':
#   app.run(debug=True)

# to see mongoDB state visually, just copy mongodb://localhost:27017/ to mongoDB Compass

from flask import Flask
from flask import request, jsonify, Response
from flask_pymongo import PyMongo
import pymongo.errors
import os
import hashlib
from threading import Thread
from DetectionServer import DetectionServer
from statistics import Statistics


app = Flask(__name__)  # Flask app

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/faceIt_DB")
db = mongodb_client.db
server = DetectionServer()
statistics = Statistics(db)

# print(FaceIt_DB.list_collection_names())
# db.todos.insert_many([
# ])


@app.route("/login")
def login():
    try:
        username = request.args.get('username')
        if db.users.find_one({"username": username}) is None:
            print("Do you already have an account?")
            return Response("wrong", status=200, mimetype='text/xml')

        provided_password = request.args.get('password')
        # get salt and key for this user
        salt = db.users.find_one({"username": username}).get('salt')
        key = db.users.find_one({"username": username}).get('key')
    except pymongo.errors.PyMongoError:
        return Response("db failure", status=400, mimetype='text/xml')

    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),  # Convert the password to bytes
        salt,
        100000
    )
    if new_key == key:
        print("Password is correct")
        thread = Thread(target=server.get_emotions, args=db)
        thread.start()
        return Response("success", status=200, mimetype='text/xml')
    else:
        print('Password is wrong')
        return Response("wrong", status=200, mimetype='text/xml')


@app.route("/register", methods=['POST'])
def register():
    try:
        username = request.form.get('userName')
        # if username is already exist in DB, return appropriate answer
        if db.users.find_one({"username": username}) is not None:
            print("username already in DB!")
            return Response("userName exists", status=400, mimetype='text/xml')

        email = request.form.get('email')
        # if email is already exist in DB, return appropriate answer
        if db.users.find_one({"email": email}) is not None:
            return Response("mail exists", status=400, mimetype='text/xml')

        salt = os.urandom(32)
        password = request.form.get('password')
        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000  # It is recommended to use at least 100,000 iterations of SHA-256
        )
        # store key and salt for this user, don't store password
        db.users.insert_one({'username': username, 'key': key, 'salt': salt, 'email': email})
        return Response("success", status=200, mimetype='text/xml')
    except pymongo.errors.PyMongoError:
        return Response("db failure", status=400, mimetype='text/xml')


@app.route("/stop", methods=['POST'])
def stop():
    checks = int(request.form.get('checks'))
    matches = int(request.form.get('matches'))
    server.stop_conversation(checks, matches)
    # todo write statistics to DB, https protocol
    if server.get_stop():
        server.set_stop_false()
        return Response("success", status=200, mimetype='text/xml')
    else:
        return Response("db failure", status=400, mimetype='text/xml')


@app.route("/statistics/user/match", methods=['GET'])
def match_user():
    user_name = request.args.get('user_name')
    time = request.args.get('time')
    match_percents = statistics.get_user_match(user_name, time)
    if match_percents is None:
        return Response("db failure", status=400, mimetype='text/xml')

    return jsonify(({'percents': match_percents}))

# def match_statistics(username):
#
#


if __name__ == '__main__':
    app.run(debug=True)
