from flask import Flask, request, jsonify
import tracemalloc
import logging

#route /project/training
def training_operations():
    if request.method == 'POST':
        # add/remove training points, start/stop/restart training
        pass
    elif request.method == 'DELETE':
        # remove training points
        pass
    elif request.method == 'GET':
        # get status of training or get results
        pass
    elif request.method == 'PUT':
        # change parameters
        pass
    return jsonify({"message": "Training operation successful"}), 200