from flask import Flask, request, jsonify
import tracemalloc
import logging

#data upload module: post
def create_project():
    # make project for data upload
    return jsonify({"message": "Project created successfully"}), 201

#route project/image, GET,POST,DELETE,PUT
def image():
    if request.method == 'GET':
        #get image
        pass
    elif request.method == 'POST':
        #post label/class data
        pass
    elif request.method == 'DELETE':
        #delete image
        pass
    elif request.method == 'PUT':
        #put image into project
        pass
    return jsonify({"message": "Image operation"}), 200
