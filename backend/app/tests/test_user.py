import unittest
from app import create_app, db
from app.models import User

class TestUserModel(unittest.TestCase):

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
        - Create sample User objects and add them to the database.
        """
        self.user1 = User(username='user1', email='user1@example.com', phone='1234567890')
        self.user1.set_password('password1')

        self.user2 = User(username='user2', email='user2@example.com', phone='9876543210')
        self.user2.set_password('password2')

        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

    def tearDown(self):
        """
        Clean up after each test case.
        - Delete sample User objects from the database.
        """
        db.session.delete(self.user1)
        db.session.delete(self.user2)
        db.session.commit()

    def test_set_password(self):
        """
        Test case for `set_password` method of User model.
        - Checks if the password is hashed and stored correctly.
        """
        self.assertNotEqual(self.user1.password, 'password1')

    def test_check_password_correct(self):
        """
        Test case for `check_password` method of User model with correct password.
        - Verifies that the method returns True for correct password.
        """
        self.assertTrue(self.user1.check_password('password1'))

    def test_check_password_incorrect(self):
        """
        Test case for `check_password` method of User model with incorrect password.
        - Verifies that the method returns False for incorrect password.
        """
        self.assertFalse(self.user1.check_password('wrongpassword'))

    def test_user_representation(self):
        """
        Test case for `__repr__` method of User model.
        - Checks if the string representation of the User object is as expected.
        """
        expected_repr = f'<User {self.user1.username}, {self.user1.email}, {self.user1.phone}>'
        self.assertEqual(repr(self.user1), expected_repr)

if __name__ == '__main__':
    unittest.main()
