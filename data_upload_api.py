from flask import Flask, request, jsonify
import tracemalloc
import logging

def create_project():
    # post project for data upload
    return jsonify({"message": "Project created successfully"}), 201
def get_image(project_id):
    # get image from project
    return jsonify({"images": "List of images"}), 200

def post_label(project_id):
    # post label/class data
    return jsonify({"message": "Label/class data posted successfully"}), 201

def delete_image(project_id, image_id):
    # delete image from project
    return jsonify({"message": "Image deleted successfully"}), 200

def put_image(project_id, image_id):
    # update image in project
    return jsonify({"message": "Image updated successfully"}), 200


