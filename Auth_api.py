from flask import Flask, request, jsonify, g
import sqlite3
import tracemalloc
import logging
import cProfile
import random
import string
from datetime import datetime

DATABASE = r'C:\Users\andre\Desktop\EC530_ML\ml.db'

app = Flask(__name__)

def generate_token(length=8):
    chars = string.ascii_letters + string.digits + string.punctuation
    tok = ''.join(random.choice(chars) for _ in range(length))
    return tok

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/new_user', methods=['POST'])
def new_user():
    logging.debug('creating new user')

    # post new user
    name = request.json['name']
    db = get_db()
    db.execute('INSERT INTO Users (name) VALUES(?)', (name))
    db.commit()

    logging.debug('user created')
    return jsonify({"message": "User created"}), 201

@app.route('/new_token', methods=['POST'])
def new_token(user_id):
    logging.debug('creating new token')

    # post token for user
    token = generate_token();
    date_made = datetime.now().date()
    db = get_db()
    db.execute('INSERT INTO Tokens (user_id, token, created) VALUES (?, ?, ?)', (user_id, token, date_made))
    db.commit();

    logging.debug('token created')
    return jsonify({"token": "Generated token"}), 201

@app.route('/get_token', methods=['GET'])
def get_token(user_id):
    logging.debug('getting user token')

    # get token
    token = query_db('SELECT token FROM Tokens WHERE user_id = ?', [user_id], one=True)
    if token is None:
        return jsonify({"error": "No token for user"}), 404
    logging.debug('token retrieved')
    return jsonify({"token": "token[0]"}), 200

@app.route('/del_user', methods=['DELETE'])
def del_user(user_id):
    logging.debug('deleting user')

    # delete user and their token/s
    db = get_db()
    db.execute('DELETE FROM Users WHERE user_id = ?' [user_id])
    db.execute('DELETE FROM Tokens WHERE user_id = ?' [user_id])
    db.commit()

    logging.debug('user deleted')
    return jsonify({"message": "User deleted successfully"}), 200


tracemalloc.start()
cProfile.run('new_user()')
cProfile.run('new_token()')
cProfile.run('get_token()')
cProfile.run('del_user()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)