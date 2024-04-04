from flask import Flask, request, jsonify, g, Blueprint
import sqlite3
import tracemalloc
import logging
import cProfile
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE = r'C:\Users\andre\Desktop\EC530_ML\diyml\Backend\ml.db'

auth_blueprint = Blueprint('auth', __name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# @auth_blueprint.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@auth_blueprint.route('/users', methods=['POST'])
def new_user():
    logging.debug('creating new user')

    # post new user
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if (query_db('SELECT id FROM Users WHERE username = ?', [username], one=True)):
        return jsonify({"error: Username not available"}), 409
    
    if (query_db('SELECT id FROM Users WHERE email = ?', [email], one=True)):
        return jsonify({"error: There is already an account associated with this email"}), 409

    hash_pass = generate_password_hash(password)
    db = get_db()
    db.execute('INSERT INTO Users (username, password, email) VALUES (?, ?, ?)', (username, hash_pass, email))
    db.commit()

    logging.debug('user created')
    return jsonify({"message": "User created"}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error: Please enter Username and Password"}), 400

    user = query_db('SELECT * FROM Users WHERE username = ?', [username], one=True)

    if user and check_password_hash(user['password'], password):
        db = get_db()
        db.execute('UPDATE Users SET active = 1, last_login = ? WHERE username = ?', (datetime.now().isoformat(), username))
        db.commit()
        return jsonify({"message" : "Logged in"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({"error": "logout failed"})
    
    if (query_db('SELECT * FROM Users WHERE user_id = ?', (user_id), one=True)):
        db = get_db()
        db.execute('UPDATE Users SET active = 0 WHERE id = ?', (user_id))
        db.commit()
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"error": "Logout Failed"}), 404

@auth_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    logging.debug('deleting user')

    # delete user and their token/s
    db = get_db()
    db.execute('DELETE FROM Users WHERE user_id = ?' [user_id])
    db.commit()

    logging.debug('user deleted')
    return jsonify({"message": "User deleted successfully"}), 200

"""
tracemalloc.start()
cProfile.run('new_user()')
cProfile.run('new_token()')
cProfile.run('get_token()')
cProfile.run('del_user()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
"""