import unittest
from flask_testing import TestCase
from flask import Flask, json
from werkzeug.datastructures import FileStorage
import io
from my_flask_app import create_app, db
from my_flask_app.models import Model, Inference

class TestInferenceAPI(TestCase):
    def create_app(self):
        # Here, you need to return an instance of your Flask app with a test configuration
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()
        # Optional: Add a dummy model for testing
        new_model = Model(project_id=1, model=b'some_binary_data', time_created='2021-01-01')
        db.session.add(new_model)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_inference(self):
        # Simulate an image upload
        data = dict(
            file=(io.BytesIO(b"fake image data"), 'test.jpg')
        )
        response = self.client.post('/inference', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 202)
        self.assertIn('Inference task submitted', response.json['message'])

    def test_get_results(self):
        # Assuming the inference ID from a previous submission is 1
        response = self.client.get('/inference/1')
        self.assertEqual(response.status_code, 200)
        # Check for specific fields in response
        self.assertIn('status', response.json['inference'])
        self.assertIn('result', response.json['inference'])

if __name__ == '__main__':
    unittest.main()
