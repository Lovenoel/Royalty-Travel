import unittest
from app import create_app, db
from app.forms import LoginForm

class TestLoginForm(unittest.TestCase):

    def setUp(self):
        # Set up a test Flask application
        self.app = create_app('testing')  # Create a Flask app configured for testing
        self.client = self.app.test_client()  # Create a test client for making requests
        self.ctx = self.app.app_context()  # Create an application context
        self.ctx.push()  # Push the context to activate it
        db.create_all()  # Create all database tables

    def tearDown(self):
        # Clean up after each test
        db.session.remove()  # Remove the session from the database
        db.drop_all()  # Drop all tables from the database
        self.ctx.pop()  # Pop the application context to deactivate it

    def test_login_form_valid(self):
        # Test a valid login form submission
        form = LoginForm(email='test@example.com', password='password123')
        self.assertTrue(form.validate())  # Assert that the form is valid

    def test_login_form_missing_email(self):
        # Test validation failure when email is missing
        form = LoginForm(password='password123')
        self.assertFalse(form.validate())  # Assert that the form is not valid

    def test_login_form_invalid_email(self):
        # Test validation failure with an invalid email format
        form = LoginForm(email='invalid_email', password='password123')
        self.assertFalse(form.validate())  # Assert that the form is not valid

    def test_login_form_short_password(self):
        # Test validation failure with a too short password
        form = LoginForm(email='test@example.com', password='short')
        self.assertFalse(form.validate())  # Assert that the form is not valid

if __name__ == '__main__':
    unittest.main()