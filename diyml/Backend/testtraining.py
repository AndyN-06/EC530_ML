import requests
import time

API_BASE_URL = "http://localhost:5000"

def start_training(project_id, dataset_id):
    response = requests.post(f"{API_BASE_URL}/training", json={
        "project_id": project_id,
        "dataset_id": dataset_id
    })
    return response.json()

def get_training_status(training_id):
    response = requests.get(f"{API_BASE_URL}/training/{training_id}")
    return response.json()

def get_training_result(training_id):
    response = requests.get(f"{API_BASE_URL}/training/{training_id}/result")
    return response.json()

def post_multiple_jobs(training_pairs):
    training_ids = []
    for pair in training_pairs:
        start_response = start_training(pair["project_id"], pair["dataset_id"])
        print("Start Training Response:", start_response)
        training_ids.append(start_response.get("training_id"))
    return training_ids

def poll_training_status(training_ids):
    results = {}
    while training_ids:
        for training_id in training_ids[:]:  # Copy to avoid modification during iteration
            status_response = get_training_status(training_id)
            print(f"Training ID {training_id} Status Response:", status_response)

        time.sleep(3)
    return results

# Define your project and dataset pairs here
training_pairs = [
    {"project_id": 1, "dataset_id": 1},
    {"project_id": 2, "dataset_id": 2},
    # Add more pairs as needed
]

# Post multiple training jobs
training_ids = post_multiple_jobs(training_pairs)

# Poll the training status until all jobs are finished
all_results = poll_training_status(training_ids)
print("All Training Results:", all_results)
