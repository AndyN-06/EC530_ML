from flask import Flask, request, jsonify

def post_inference():
    # post inference
    return jsonify({"message": "Inference posted successfully"}), 201

def get_inference():
    # get inference
    return jsonify({"inference": "Inference details"}), 200

def delete_inference():
    # delete inference
    return jsonify({"message": "Inference deleted successfully"}), 200