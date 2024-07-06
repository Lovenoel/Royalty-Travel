import unittest
from flask import Flask, session
from flask_testing import TestCase
from app import create_app, db
from app.models import User
from io import BytesIO

class ProfileRoutesTestCase(TestCase):

    def create_app(self):
        """Create an instance of the Flask application for testing."""
        app = create_app('testing')  # Create a Flask app with 'testing' configuration
        app.config['TESTING'] = True  # Set TESTING to True for Flask Testing configuration
        return app

    def setUp(self):
        """Set up the test environment."""
        db.create_all()  # Create all tables in the test database
        # Create a test user
        self.user = User(username='test_user', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()  # Remove the session from the database
        db.drop_all()  # Drop all tables from the database

    def login(self):
        """Simulate user login for testing purposes."""
        with self.client:
            self.client.post('/login', data=dict(
                email='test@example.com',
                password='password123'
            ), follow_redirects=True)

    def test_profile_update(self):
        """Test updating user profile."""
        self.login()  # Log in the user
        with self.client:
            response = self.client.post('/profile/profile', data=dict(
                name='Updated Name',
                email='updated@example.com',
                phone='1234567890'
            ), follow_redirects=True)
            # Assert that the response contains the success message
            self.assertIn(b'Your profile has been updated!', response.data)
            self.assertEqual(response.status_code, 200)
            # Retrieve the updated user from the database and verify changes
            updated_user = User.query.filter_by(username='test_user').first()
            self.assertEqual(updated_user.name, 'Updated Name')
            self.assertEqual(updated_user.email, 'updated@example.com')
            self.assertEqual(updated_user.phone, '1234567890')

    def test_change_password(self):
        """Test changing user password."""
        self.login()  # Log in the user
        with self.client:
            response = self.client.post('/profile/change_password', data=dict(
                current_password='password123',
                new_password='newpassword123',
                confirm_password='newpassword123'
            ), follow_redirects=True)
            # Assert that the response contains the success message
            self.assertIn(b'Your password has been updated!', response.data)
            self.assertEqual(response.status_code, 200)
            # Retrieve the updated user from the database and verify password change
            updated_user = User.query.filter_by(username='test_user').first()
            self.assertTrue(updated_user.check_password('newpassword123'))

    def test_upload_profile_picture(self):
        """Test uploading a profile picture."""
        self.login()  # Log in the user
        with self.client:
            data = dict(
                profile_picture=(BytesIO(b'dummy_image_content'), 'test_image.jpg')
            )
            response = self.client.post('/profile/upload_picture', data=data, content_type='multipart/form-data')
            # Assert that the response contains the success message
            self.assertIn(b'File successfully uploaded', response.data)
            self.assertEqual(response.status_code, 200)

    def test_upload_profile_picture_no_file_part(self):
        """Test uploading a profile picture when no file is provided."""
        self.login()  # Log in the user
        with self.client:
            response = self.client.post('/profile/upload_picture')
            # Assert that the response contains an error message indicating no file part
            self.assertIn(b'No file part', response.data)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
