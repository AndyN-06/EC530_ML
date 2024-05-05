import unittest
from flask_testing import TestCase
from my_flask_app import create_app, db 
from flask import json
from my_flask_app.models import Project

class TestTrainingAPI(TestCase):
    def create_app(self):
        # Here, you need to return an instance of your Flask app with a test configuration
        app = create_app('testing')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for tests
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()
        # Optional: Add a dummy project for testing
        new_project = Project(name='Test Project', user_id=1)
        db.session.add(new_project)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_start_training(self):
        # Assuming the project ID for 'Test Project' is 1
        response = self.client.post('/training', json={'project_id': 1})
        self.assertEqual(response.status_code, 202)
        self.assertIn('Training started successfully', response.json['message'])

if __name__ == '__main__':
    unittest.main()
