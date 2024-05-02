from flask import Flask, request, jsonify, g, Blueprint, current_app
import sqlite3
import tracemalloc
import logging
import cProfile
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

# configure logging
logging.basicConfig(level=logging.DEBUG)

DB = 'ml.db'
DATABASE = os.path.join(os.path.dirname(__file__), DB)
auth_blueprint = Blueprint('auth', __name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@auth_blueprint.route('/users', methods=['POST'])
def new_user():
    data = request.json
    current_app.logger.info(f'Received username: {data.get("username")}')
    current_app.logger.info(f'Received password: {data.get("password")}')
    current_app.logger.info(f'Received email: {data.get("email")}')

    # post new user
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if (query_db('SELECT user_id FROM Users WHERE username = ?', [username], one=True)):
        return jsonify({"error: Username not available"}), 409
    
    if (query_db('SELECT user_id FROM Users WHERE email = ?', [email], one=True)):
        return jsonify({"error: There is already an account associated with this email"}), 409

    # hash_pass = generate_password_hash(password)
    db = get_db()
    db.execute('INSERT INTO Users (username, password, email, active) VALUES (?, ?, ?, 0)', (username, password, email))
    db.commit()

    current_app.logger.info('user created')
    return jsonify({"message": "User created"}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    current_app.logger.info('logging in')
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error: Please enter Username and Password"}), 400

    correct = query_db('SELECT * FROM Users WHERE username = ? AND password = ?', [username, password], one=True)

    if correct:
        db = get_db()
        db.execute('UPDATE Users SET active = 1, last_login = ? WHERE username = ?', (datetime.now().isoformat(), username))
        db.commit()
        return jsonify({"message" : "Logged in"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    current_app.logger.info('logging out')
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
    current_app.logger.info('deleting user')

    # delete user and their token/s
    db = get_db()
    db.execute('DELETE FROM Users WHERE user_id = ?' [user_id])
    db.commit()

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