import unittest
from app import create_app, db
from app.models import User
from app.forms import RegistrationForm

class TestRegistration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.
        - Creates a Flask application instance for testing.
        - Sets up a test client to simulate requests.
        - Establishes an application context.
        - Creates all database tables.
        """
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the test environment after all tests.
        - Removes the application context.
        - Drops all database tables.
        """
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def setUp(self):
        """
        Set up before each test case.
        - Create sample data and add it to the database.
        """
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

    def tearDown(self):
        """
        Clean up after each test case.
        - Delete sample data from the database.
        """
        User.query.delete()
        db.session.commit()

    def test_registration_form_valid(self):
        """
        Test case for successful user registration with valid form data.
        """
        form = RegistrationForm(data=self.user_data)
        self.assertTrue(form.validate())

    def test_registration_form_missing_username(self):
        """
        Test case for user registration with missing username.
        """
        del self.user_data['username']
        form = RegistrationForm(data=self.user_data)
        self.assertFalse(form.validate())
        self.assertIn('Username is required', form.username.errors)

    def test_registration_form_invalid_email(self):
        """
        Test case for user registration with invalid email format.
        """
        self.user_data['email'] = 'invalid_email_format'
        form = RegistrationForm(data=self.user_data)
        self.assertFalse(form.validate())
        self.assertIn('Invalid email address', form.email.errors)

    def test_registration_form_password_mismatch(self):
        """
        Test case for user registration with password and confirm password mismatch.
        """
        self.user_data['confirm_password'] = 'mismatched_password'
        form = RegistrationForm(data=self.user_data)
        self.assertFalse(form.validate())
        self.assertIn('Passwords must match', form.confirm_password.errors)

    def test_registration_route_post(self):
        """
        Test case for POST request to user registration route.
        """
        response = self.client.post('/register', data=self.user_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Check if registration is successful (redirects to login page)

if __name__ == '__main__':
    unittest.main()
