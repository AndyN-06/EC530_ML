from flask import Flask, request, jsonify

def post_test():
    # post new test for a model
    return jsonify({"message": "Test posted successfully"}), 201

def get_test():
    # get results from test
    return jsonify({"test": "Test details"}), 200
