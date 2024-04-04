from flask import Flask, request, jsonify
import tracemalloc
import logging
import cProfile

def post_report():
    logging.debug('posting report')
    # post report
    logging.debug('report posted')
    return jsonify({"message": "Report posted successfully"}), 201

def get_report():
    logging.debug('getting report')
    # get report
    logging.debug('report retrieved')
    return jsonify({"report": "Report details"}), 200

def delete_report():
    logging.debug('deleting report')
    # delete report
    logging.debug('report deleted')
    return jsonify({"message": "Report deleted successfully"}), 200

tracemalloc.start()
cProfile.run('post_report()')
cProfile.run('get_report()')
cProfile.run('delete_report()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)