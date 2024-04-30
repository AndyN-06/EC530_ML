from flask import Flask, request, jsonify, g, Blueprint, current_app
from sqlite3 import connect, Row
from datetime import datetime
import threading
import time
from queue import Queue
from contextlib import contextmanager
import tracemalloc
import logging
import cProfile
import os

DB = 'ml.db'
DATABASE = os.path.join(os.path.dirname(__file__), DB)
train_blueprint = Blueprint('train', __name__)
db_queue = Queue()

def get_db():
    if 'db' not in g:
        g.db = connect(DATABASE, check_same_thread=False)
        g.db.row_factory = Row
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False, commit=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if commit:
        db.commit()
    return (rv[0] if rv else None) if one else rv

@contextmanager
def app_context():
    with app.app_context():
        yield

def update_status(training_id, status):
    print("update")
    query_db('UPDATE Training SET status = ? WHERE training_id = ?', (status, training_id), commit=True)  

def train(task_info):
    print("training")
    training_id = task_info["training_id"]
    update_status(training_id, 'in progress')

    # train
    time.sleep(5)

    update_status(training_id, 'finished')
    print(f"Training {training_id} done at {datetime.now()}")

def worker():
    while True:
        task_info = db_queue.get()
        with app_context():
            try:
                train(task_info)
            finally:
                db_queue.task_done()

@app.route('/configs', methods=['POST'])
def new_param():
    logging.debug("changing training parameters")
    
    # post new training parameters
    data = request.json
    proj_id = data.get('project_id')
    name = data.get('name')
    val = data.get('value')
    db = get_db()
    db.execute('INSERT INTO Configurations (project_id, name, value) VALUES (?, ?, ?)', (proj_id, name, val))
    db.commit()

    logging.debug("finished changing training parameters")
    return jsonify({"message": "Training parameters updated successfully"}), 200

@app.route('/configs/<int:configuration_id>', methods=['DELETE'])
def delete_param(configuration_id):
    print("del")
    logging.debug('deleting param')

    # delete inference
    query_db('DELETE FROM COnfigurations WHERE configuration_id = ?', [configuration_id], commit=True)

    logging.debug('inference deleted')
    return jsonify({"message": "Inference deleted successfully"}), 200

@app.route('/training', methods=['POST'])
def start_training():
    print("post")
    logging.debug("started training")
    
    # post new training session
    data = request.json
    proj_id = data.get('project_id')
    dataset = data.get('dataset_id')

    with get_db() as db:
        cur = db.execute('''INSERT INTO Training (project_id, start_time, status) VALUES (?, ?, 'pending')''', (proj_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        db.commit()
        training_id = cur.lastrowid
        cur.close()

    task_info = {"training_id": training_id, "dataset_id": dataset}    
    db_queue.put(task_info)

    return jsonify({"message": "Training started successfully"}), 202

def stop_training():
    logging.debug("stopped training")
    # put to stop current training
    return jsonify({"message": "Training stopped successfully"}), 200

def restart_training():
    logging.debug("restarted training")
    # put resume or restart training
    return jsonify({"message": "Training restarted successfully"}), 202

@app.route('/training/<int:training_id>', methods=['GET'])
def get_status(training_id):
    logging.debug("getting status of training")
    
    # get status of training
    query = 'SELECT status FROM Training WHERE training_id = ?'
    row = query_db(query, [training_id], one=True)
    if row is None:
        return jsonify({"error": "Training not found"}), 404
    status = row['status']
    logging.debug('training retrieved')
    return jsonify({"training": {"status": status}}), 200

@app.route('/training/<int:training_id>/result', methods=['GET'])
def get_results():
    logging.debug("getting results of training")
    
    # get results of training
    row = query_db('SELECT result FROM Training WHERE training_id = ?', [training_id], one=True)
    if row is None:
        return jsonify({"error": "Training not found"}), 404
    result = row['result']
    logging.debug("got results of training")
    return jsonify({"result": result}), 200

@app.route('/training/<int:training_id>', methods=['DELETE'])
def delete_training(training_id):
    query_db('DELETE FROM Training WHERE training_id = ?', [training_id])
    return jsonify({"message": "Training deleted successfully"}), 202

threading.Thread(target=worker, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)

"""
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
"""