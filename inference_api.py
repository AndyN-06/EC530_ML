from flask import Flask, request, jsonify, g
from sqlite3 import connect, Row
from datetime import datetime
import threading
import time
from queue import Queue
from contextlib import contextmanager
import logging
import cProfile
import tracemalloc

app = Flask(__name__)
# DATABASE = r'C:\Users\andre\Desktop\EC530_ML\ml.db'
DATABASE = '/usr/src/app/ml.db'
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

def update_status(inference_id, status):
    print("update")
    query_db('UPDATE Inferences SET status = ? WHERE inference_id = ?', (status, inference_id), commit=True)

def do_inference(task_info):
    print("do infer")
    inference_id = task_info["inference_id"]
    update_status(inference_id, 'in progress')
    # Simulate a long-running inference task
    time.sleep(2)  # Simulate inference time
    update_status(inference_id, 'finished')
    print(f"Inference {inference_id} done at {datetime.now()}")


def worker():
    print("doing in back")
    while True:
        task_info = db_queue.get()
        with app_context():
            try:
                do_inference(task_info)
            finally:
                db_queue.task_done()

@app.route('/inference', methods=['POST'])
def post_inference():
    print("post")
    data = request.json
    model_id = data.get('model_id')
    image_id = 1  # Dummy value for example purposes

    with get_db() as db:
        cur = db.execute('''INSERT INTO Inferences (model_id, image_id, status, inferred_at) VALUES (?, ?, 'pending', ?)''',
                         (model_id, image_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        db.commit()
        inference_id = cur.lastrowid
        cur.close()

    # Add the task to the queue
    task_info = {"inference_id": inference_id, "model_id": model_id}
    db_queue.put(task_info)

    return jsonify({"message": "Inference task submitted.", "inference_id": inference_id}), 202

@app.route('/inference/<int:inference_id>', methods=['GET'])
def get_inference(inference_id):
    print("get")
    logging.debug('getting inference')
    # get inference status and result
    query = 'SELECT status, result FROM Inferences WHERE inference_id = ?'
    row = query_db(query, [inference_id], one=True)
    if row is None:
        return jsonify({"error": "Inference not found"}), 404
    # Assuming 'result' could be None if inference is not finished yet
    status, result = row
    logging.debug('inference retrieved')
    return jsonify({"inference": {"status": status, "result": result}}), 200


@app.route('/inference/<int:inference_id>', methods=['DELETE'])
def delete_inference(inference_id):
    print("del")
    logging.debug('deleting inference')

    # delete inference
    query_db('DELETE FROM Inferences WHERE inference_id = ?', [inference_id], commit=True)

    logging.debug('inference deleted')
    return jsonify({"message": "Inference deleted successfully"}), 200

# Start the worker thread
threading.Thread(target=worker, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)

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