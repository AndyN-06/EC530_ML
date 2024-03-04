from flask import Flask, request, jsonify
import tracemalloc
import logging
import cProfile

def post_test():
    logging.debug('starting new test')
    # post new test for a model
    logging.debug('test finished')
    return jsonify({"message": "Test posted successfully"}), 201

def get_test():
    logging.debug('getting test results')
    # get results from test
    logging.debug('test results retrieved')
    return jsonify({"test": "Test details"}), 200

tracemalloc.start()
cProfile.run('post_test()')
cProfile.run('get_test()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)