from flask import Flask, request, jsonify
import tracemalloc
import logging
import cProfile

def post_inference():
    logging.debug('posting inference')
    # post inference
    logging.debug('inference posted')
    return jsonify({"message": "Inference posted successfully"}), 201

def get_inference():
    logging.debug('getting inference')
    # get inference
    logging.debug('inference retrieved')
    return jsonify({"inference": "Inference details"}), 200

def delete_inference():
    logging.debug('deleting inference')
    # delete inference
    logging.debug('inference deleted')
    return jsonify({"message": "Inference deleted successfully"}), 200

tracemalloc.start()
cProfile.run('post_inference()')
cProfile.run('get_inference()')
cProfile.run('delete_inference()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)