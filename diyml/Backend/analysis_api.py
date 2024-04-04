from flask import Flask, request, jsonify
import tracemalloc
import logging
import cProfile

def post_analysis():
    logging.debug('posting analysis')
    # analyze data
    logging.debug('analysis posted')
    return jsonify({"analysis": "Data analysis results"}), 200

tracemalloc.start()
cProfile.run('post_analysis()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)