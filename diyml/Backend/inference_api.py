from flask import Flask, request, jsonify, g, Blueprint, current_app
from sqlite3 import connect, Row
from datetime import datetime
import threading
import time
from queue import Queue
from contextlib import contextmanager
import logging
import cProfile
import tracemalloc
import os
from infer_algo import predict

infer_blueprint = Blueprint('inference', __name__)

DB = 'ml.db'
DATABASE = os.path.join(os.path.dirname(__file__), DB)
db_queue = Queue()

def get_db():
    if 'db' not in g:
        g.db = connect(DATABASE, check_same_thread=False)
        g.db.row_factory = Row
    return g.db

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
    with current_app.app_context():
        yield

def update_status(inference_id, status):
    query_db('UPDATE Inferences SET status = ? WHERE inference_id = ?', (status, inference_id), commit=True)


def worker():
    while True:
        task_info = db_queue.get()
        with app_context():
            try:
                do_inference(task_info)
            finally:
                db_queue.task_done()

def do_inference(task_info):
    inference_id = task_info["inference_id"]
    update_status(inference_id, 'in progress')

    predict(task_info["project_id"], task_info["image_path"])

    update_status(inference_id, 'finished')
    print(f"Inference {inference_id} done at {datetime.now()}")


@infer_blueprint.route('/inference', methods=['POST'])
def post_inference(model_id, project_id):
    data = request.files['file']
    folder = 'uploads'
    folder = os.path.join(os.path.dirname(__file__), folder)
    img_path = os.path.join(folder, data.filename)
    data.save(img_path)

    with get_db() as db:
        cur = db.execute('INSERT INTO Inferences (model_id, image_path) VALUES (?, ?)',(model_id, img_path))
        db.commit()
        inference_id = cur.lastrowid
        cur.close()

    # Add the task to the queue
    task_info = {"inference_id": inference_id, "project_id": project_id, "image_path": img_path}
    db_queue.put(task_info)

    return jsonify({"message": "Inference task submitted.", "inference_id": inference_id}), 202

@infer_blueprint.route('/inference/<int:inference_id>', methods=['GET'])
def get_results(inference_id):
    # logging.debug('getting inference')
    
    # get inference status and result
    query = 'SELECT status, result FROM Inferences WHERE inference_id = ?'
    row = query_db(query, [inference_id], one=True)
    if row is None:
        return jsonify({"error": "Inference not found"}), 404
    # Assuming 'result' could be None if inference is not finished yet
    status, result = row
    
    # logging.debug('inference retrieved')
    return jsonify({"inference": {"status": status, "result": result}}), 200

# Start the worker thread
threading.Thread(target=worker, daemon=True).start()


# @infer_blueprint.route('/inference/<int:inference_id>', methods=['DELETE'])
# def delete_inference(inference_id):
#     logging.debug('deleting inference')

#     # delete inference
#     query_db('DELETE FROM Inferences WHERE inference_id = ?', [inference_id], commit=True)

#     logging.debug('inference deleted')
#     return jsonify({"message": "Inference deleted successfully"}), 200



"""
tracemalloc.start()
cProfile.run('post_inference()')
cProfile.run('get_inference()')
cProfile.run('delete_inference()')
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
"""