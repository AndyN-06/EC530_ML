from flask import Flask, request, jsonify, g
import sqlite3
import tracemalloc
import logging
import cProfile
from datetime import datetime


DATABASE = r'C:\Users\andre\Desktop\EC530_ML\ml.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/projects', methods=['POST'])
def create_project(user_id):
    logging.debug('creating project')

    # post project for data upload
    name = request.json["name"]
    date_made = datetime.now().date()
    db = get_db()
    db.execute('INSERT INTO Projects (user_id, name, created) VALUES (?, ?, ?)', (user_id, name, date_made))
    db.commit()

    logging.debug('project created')
    return jsonify({"message": "Project created successfully"}), 201

@app.route('/images/<int:project_id>', methods=['GET'])
def get_image(project_id):
    logging.debug('getting image')

    # get image from project
    db = get_db()
    imgs = db.execute('SELECT image_id FROM Images WHERE project_id = ?', (project_id,)).fetchall()

    logging.debug('image retrieved')
    return jsonify({"images": imgs}), 200

@app.route('/labels/<int:project_id>', methods=['POST'])
def post_label(project_id):
    logging.debug('adding label')

    # post label/class data
    data = request.json
    db = get_db()
    db.execute('INSERT INTO Labels (image_id, label) VALUES (?, ?)', (data['image_id'], data['label']))
    db.commit()

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