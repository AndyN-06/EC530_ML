from flask import Flask, request, jsonify

def post_model():
    # post model
    return jsonify({"message": "Model posted successfully"}), 201

def get_model():
    # get model
    return jsonify({"model": "Model details"}), 200

def delete_model():
    # delete model
    return jsonify({"message": "Model deleted successfully"}), 200