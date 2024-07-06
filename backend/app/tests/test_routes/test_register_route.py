import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class RegistrationTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up the test environment."""
        self.app = create_app('testing')  # Create a Flask app instance with 'testing' configuration
        self.client = self.app.test_client()  # Create a test client for making requests
        self.app_context = self.app.app_context()  # Push an application context
        self.app_context.push()
        db.create_all()  # Create all tables in the test database

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()  # Remove the current session from the database
        db.drop_all()  # Drop all tables from the database
        self.app_context.pop()  # Pop the application context

    def test_register_get(self):
        """Test GET request to registration page."""
        response = self.client.get(url_for('register.register'))  # Send a GET request to the registration page
        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200 (OK)
        self.assertIn(b'Register', response.data)  # Assert that the word 'Register' is in the response data

    def test_register_post(self):
        """Test POST request to registration page."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone': '1234567890',
            'password': 'password',
            'confirm_password': 'password'
        }
        response = self.client.post(url_for('register.register'), data=data, follow_redirects=True)
        # Send a POST request to the registration page with form data and follow redirects
        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200 (OK)
        self.assertIn(b'Congratulations, you are welcome to Royalty Travel', response.data)
        # Assert that the success message is in the response data

        # Check if user is added to the database
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)  # Assert that user object is not None (user exists)
        self.assertEqual(user.username, 'testuser')  # Assert that the username is correct

if __name__ == '__main__':
    unittest.main()
