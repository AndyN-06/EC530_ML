import pytest
from quart.testing import QuartClient
from inference_api import app
import asyncio

@pytest.fixture
def client():
    return QuartClient(app)

@pytest.fixture
async def test_post_inference(client):
    response = await client.post('/inference', json={'model_id': 1, 'image': 'dummy_image_data'})
    assert response.status_code == 202
    response_data = await response.get_json()
    return response_data["inference_id"]

@pytest.mark.asyncio
async def test_inference_queue_processing(client, test_post_inference):
    # Submit multiple jobs and collect their inference IDs
    inference_ids = []

    # Poll each job's status until it becomes 'finished'
    for _ in range(3):
        inference_id = await test_post_inference
        inference_ids.append(inference_id)
        status = 'pending'
        while status != 'finished':
            response = await client.get(f'/inference/{inference_id}')
            assert response.status_code == 200
            response_data = await response.get_json()
            status = response_data["inference"]["status"]
            if status != 'finished':
                await asyncio.sleep(0.1)  # Short delay before polling again

@pytest.mark.asyncio
async def test_delete_inference(client, test_post_inference):
    inference_id = await test_post_inference
    response = await client.delete(f'/inference/{inference_id}')
    assert response.status_code == 200
    response_data = await response.get_json()
    assert response_data["message"] == "Inference deleted successfully"
