from flask import Flask, request, jsonify
import tracemalloc
import logging
import cProfile

def add_points():
    logging.debug("adding training points")
    # post training points
    logging.debug("finished adding training points")
    return jsonify({"message": "Training points added successfully"}), 200

def rem_points():
    logging.debug("removing training points")
    # delete training points
    logging.debug("finished removing training points")
    return jsonify({"message": "Training points removed successfully"}), 200

def change_param():
    logging.debug("changing training parameters")
    # put changes to training parameters
    logging.debug("finished changing training parameters")
    return jsonify({"message": "Training parameters updated successfully"}), 200

def start_training():
    logging.debug("started training")
    # post new training session
    return jsonify({"message": "Training started successfully"}), 202

def stop_training():
    logging.debug("stopped training")
    # put to stop current training
    return jsonify({"message": "Training stopped successfully"}), 200

def restart_training():
    logging.debug("restarted training")
    # put resume or restart training
    return jsonify({"message": "Training restarted successfully"}), 202

def get_status():
    logging.debug("getting status of training")
    # get status of training
    logging.debug("got status of training")
    return jsonify({"status": "Training status"}), 200

def get_results():
    logging.debug("getting results of training")
    # get results of training
    logging.debug("got results of training")
    return jsonify({"results": "Training results"}), 200

tracemalloc.start()
cProfile.run('add_points()')
cProfile.run('rem_points()')
cProfile.run('change_param()')
cProfile.run('start_training()')
cProfile.run('stop_training()')
cProfile.run('restart_training()')
cProfile.run('get_status()')
cProfile.run('get_results()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)