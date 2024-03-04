from flask import Flask, request, jsonify
import tracemalloc
import logging
import cProfile

def post_model():
    logging.debug('posting model')
    # post model
    logging.debug('model posted')
    return jsonify({"message": "Model posted successfully"}), 201

def get_model():
    logging.debug('getting model')
    # get model
    logging.debug('model details retrieved')
    return jsonify({"model": "Model details"}), 200

def delete_model():
    logging.debug('deleting model')
    # delete model
    logging.debug('model deleted')
    return jsonify({"message": "Model deleted successfully"}), 200

tracemalloc.start()
cProfile.run('post_model()')
cProfile.run('get_model()')
cProfile.run('delete_model()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)