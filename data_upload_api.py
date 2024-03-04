from flask import Flask, request, jsonify
import tracemalloc
import logging
import cProfile

def create_project():
    logging.debug('creating project')
    # post project for data upload
    logging.debug('project created')
    return jsonify({"message": "Project created successfully"}), 201
def get_image(project_id):
    logging.debug('getting image')
    # get image from project
    logging.debug('image retrieved')
    return jsonify({"images": "List of images"}), 200

def post_label(project_id):
    logging.debug('adding label')
    # post label/class data
    logging.debug('label added')
    return jsonify({"message": "Label/class data posted successfully"}), 201

def delete_image(project_id, image_id):
    logging.debug('deleting image')
    # delete image from project
    logging.debug('image deleted')
    return jsonify({"message": "Image deleted successfully"}), 200

def put_image(project_id, image_id):
    logging.debug('adding image')
    # update image in project
    logging.debug('image added')
    return jsonify({"message": "Image updated successfully"}), 200

tracemalloc.start()
cProfile.run('create_project()')
cProfile.run('get_image()')
cProfile.run('post_label()')
cProfile.run('delete_image()')
cProfile.run('put_image()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)