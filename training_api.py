from flask import Flask, request, jsonify
import tracemalloc
import logging

def add_points():
    # post training points
    return jsonify({"message": "Training points added successfully"}), 200

def rem_points():
    # delete training points
    return jsonify({"message": "Training points removed successfully"}), 200

def change_param():
    # put changes to training parameters
    return jsonify({"message": "Training parameters updated successfully"}), 200

def start_training():
    # post new training session
    return jsonify({"message": "Training started successfully"}), 202

def stop_training():
    # put to stop current training
    return jsonify({"message": "Training stopped successfully"}), 200

def restart_training():
    # put resume or restart training
    return jsonify({"message": "Training restarted successfully"}), 202

def get_status():
    # get status of training
    return jsonify({"status": "Training status"}), 200

def get_results():
    # get results of training
    return jsonify({"results": "Training results"}), 200

