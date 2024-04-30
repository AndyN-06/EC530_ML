from flask import Flask, request, jsonify, g, Blueprint, current_app
import sqlite3
import tracemalloc
import logging
import cProfile
from datetime import datetime
import os

# upload image for training with label
# upload image for testing without label
# remove image from database
# create new project
# edit image label

# configure logging
logging.basicConfig(level=logging.DEBUG)

# database path
DB = 'ml.db'
DATABASE = os.path.join(os.path.dirname(__file__), DB)

# flask app blueprint
upload_blueprint = Blueprint('upload', __name__)

### database access helper functions ###
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


### data upload functions ###
@upload_blueprint.route('/projects', methods=['POST'])
def create_project(user_id):
    current_app.logger.info("creating project")
    
    try:
        data = request.json
        name = data.get("name")

        if not name:
            return jsonify({"error": "Name required"}), 400
        
        db = get_db()
        db.execute('INSERT INTO Projects (user_id, name) VALUES (?, ?)', (user_id, name))
        db.commit()

        current_app.logger.info("project created")
        return jsonify({"message": "Project created successfully"}), 201
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({"error": "Internal Server Error"}), 500
    
@upload_blueprint.route('/upload/train', methods=['POST'])
def upload_train(project_id):
    current_app.logger.info("uploading image")

    try:
        file = request.files['file']
        img = file.read()
        data = request.json
        label = data.get("label")

        if not img or not label:
            return jsonify({"error": "Image and label are required"}), 400

        db = get_db()
        db.execute('INSERT INTO Images (project_id, image, label) VALUES (?, ?, ?)', (project_id, img, label))
        db.commit()

        current_app.logger.info("image uploaded")
        return jsonify({"message": "Image updated successfully"}), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@upload_blueprint.route('/upload/test', methods=['POST'])
def upload_test(project_id):
    # update image in project
    return jsonify({"message": "Image updated successfully"}), 200

@upload_blueprint.route('/image/<int:image_id>', methods=['DELETE'])
def del_image(image_id):
    current_app.logger.info("deleting image")
    try:
        db = get_db()
        db.execute('DELETE FROM Images WHERE image_id = ?', (image_id,))
        db.commit()
        
        current_app.logger.info("image deleted")
        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@upload_blueprint.route('/image/<int:image_id>/label', methods=['PUT'])
def edit_label(image_id):
    current_app.logger.info("changing label")

    # post label/class data
    try:
        data = request.json
        label = data.get("label")
        if not label:
            return jsonify({"error": "Label is required"}), 400
        
        db = get_db()
        db.execute('UPDATE Images SET label = ? WHERE image_id = ?', (label, image_id))
        db.commit()
        
        current_app.logger.info("label changed")
        return jsonify({"message": "Label updated successfully"}), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({"error": "Internal Server Error"}), 500
    
# tracemalloc.start()
# cProfile.run('create_project()')
# cProfile.run('get_image()')
# cProfile.run('post_label()')
# cProfile.run('delete_image()')
# cProfile.run('put_image()')
# snapshot = tracemalloc.take_snapshot()

# top_stats = snapshot.statistics('lineno')
# for stat in top_stats[:10]:
#     print(stat)