import unittest
from flask_testing import TestCase
from my_app import create_app, db  # Adjust the import according to your actual app structure
from flask import json

class TestUploadAPI(TestCase):
    def create_app(self):
        # Here you need to return an instance of your Flask app with a test configuration
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        # Optional: Add a dummy user and project for testing
        self.client.post('/projects', json={'name': 'Test Project', 'user_id': 1})

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_project(self):
        response = self.client.post('/projects', json={'name': 'New Project', 'user_id': 1})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Project created successfully', response.json['message'])

    def test_upload_train(self):
        # Assuming you have a project id 1 already from setUp
        data = {
            'label': 'cat'
        }
        response = self.client.post('/upload/train', data=data, content_type='multipart/form-data',
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Image updated successfully', response.json['message'])

    def test_del_image(self):
        # First, add an image
        self.client.post('/upload/train', data={'project_id': 1, 'image': (io.BytesIO(b"abcdef"), 'test.jpg'), 'label': 'cat'}, content_type='multipart/form-data')
        # Then delete it
        response = self.client.delete('/image/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Image deleted successfully', response.json['message'])

    def test_edit_label(self):
        # First, add an image
        self.client.post('/upload/train', data={'project_id': 1, 'image': (io.BytesIO(b"abcdef"), 'test.jpg'), 'label': 'cat'}, content_type='multipart/form-data')
        # Then change its label
        response = self.client.put('/image/1/label', json={'label': 'dog'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Label updated successfully', response.json['message'])

if __name__ == '__main__':
    unittest.main()
