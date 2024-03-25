import requests
import sqlite3
import time

# Replace with the actual endpoint if the app is running on a different host/port
INFER_API_URL = 'http://127.0.0.1:5000/inference'
DELETE_URL = 'http://127.0.0.1:5000/inference/{}'  # Assuming there's an endpoint to delete inferences
DATABASE_PATH = r'C:\Users\andre\Desktop\EC530_ML\ml.db'

def post_inference_job(model_id, image_data):
    response = requests.post(INFER_API_URL, json={'model_id': model_id, 'image': image_data})
    if response.status_code == 202:
        return response.json()['inference_id']
    else:
        raise Exception(f"Failed to post inference job. Status Code: {response.status_code}")

def get_inference_status(inference_id):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT status FROM Inferences WHERE inference_id = ?", (inference_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row['status'] if row else 'Not Found'

def delete_inference(inference_id):
    response = requests.delete(DELETE_URL.format(inference_id))
    return response.status_code

if __name__ == '__main__':
    # Post multiple inference jobs and collect their IDs
    inference_ids = [post_inference_job(model_id=1, image_data='dummy_image_data') for _ in range(4)]
    
    # Wait for all jobs to be processed
    all_processed = False
    while not all_processed:
        all_processed = all(get_inference_status(inf_id) == 'finished' for inf_id in inference_ids)
        time.sleep(1)  # Check every second

    # Test deleting an inference
    delete_status_code = delete_inference(inference_ids[0])
    assert delete_status_code == 200, f"Failed to delete inference. Status Code: {delete_status_code}"
    print("Inference deleted successfully.")

    print("All tests passed!")