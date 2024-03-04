from flask import Flask, request, jsonify
import tracemalloc
import logging
import cProfile

def new_user():
    logging.debug('creating new user')
    # post new user
    logging.debug('user created')
    return jsonify({"message": "User created"}), 201

def new_token():
    logging.debug('creating new token')
    # post token for user
    logging.debug('token created')
    return jsonify({"token": "Generated token"}), 201

def get_token():
    logging.debug('getting user token')
    # get token
    logging.debug('token retrieved')
    return jsonify({"token": "Retrieved token"}), 200

def del_user():
    logging.debug('deleting user')
    # delete user and their token/s
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