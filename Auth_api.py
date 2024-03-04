from flask import Flask, request, jsonify

def new_user():
    # post new user
    return jsonify({"message": "User created"}), 201

def new_token():
    # post token for user
    return jsonify({"token": "Generated token"}), 201

def get_token():
    # get token
    return jsonify({"token": "Retrieved token"}), 200

def del_user():
    # delete user and their token/s
    return jsonify({"message": "User deleted successfully"}), 200