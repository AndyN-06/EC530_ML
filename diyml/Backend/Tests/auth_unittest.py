import unittest
from flask_testing import TestCase
from my_flask_app import create_app, db 
from my_flask_app.models import User

class TestUserAPI(TestCase):
    def create_app(self):
        # Here you need to return an instance of your Flask app with a test configuration
        app = create_app('testing')  # Adjust this to match your application factory pattern
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for tests
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_new_user(self):
        # Successful user creation
        response = self.client.post('/users', json={
            'username': 'testuser',
            'password': 'strongpassword',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json['message'])

        # Test duplicate username
        response = self.client.post('/users', json={
            'username': 'testuser',
            'password': 'anotherstrongpassword',
            'email': 'test2@example.com'
        })
        self.assertEqual(response.status_code, 409)

        # Test duplicate email
        response = self.client.post('/users', json={
            'username': 'testuser2',
            'password': 'anotherstrongpassword',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 409)

if __name__ == '__main__':
    unittest.main()
