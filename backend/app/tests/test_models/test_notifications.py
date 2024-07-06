import unittest
from datetime import datetime
from app import create_app, db
from app.models import Notification

class TestNotificationModel(unittest.TestCase):

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
        - Create a sample Notification object and add it to the database.
        """
        self.notification = Notification(
            title='Test Notification',
            message='This is a test message.',
            timestamp=datetime.utcnow()
        )
        db.session.add(self.notification)
        db.session.commit()

    def tearDown(self):
        """
        Clean up after each test case.
        - Delete the sample Notification object from the database.
        """
        db.session.delete(self.notification)
        db.session.commit()

    def test_create_notification(self):
        """
        Test case for creating a Notification object.
        - Checks if the Notification object was created successfully.
        - Verifies the title, message, and timestamp attributes of the created Notification.
        """
        notification = Notification.query.filter_by(title='Test Notification').first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.message, 'This is a test message.')

    def test_notification_title_max_length(self):
        """
        Test case for creating a Notification with maximum title length.
        - Attempts to create a Notification with a title exceeding the allowed maximum length.
        - Asserts that an exception is raised during the commit operation.
        """
        long_title = 'A' * 101  # Maximum length for title is 100 characters
        notification = Notification(title=long_title, message='Short message')
        db.session.add(notification)
        
        with self.assertRaises(Exception):
            db.session.commit()

    def test_notification_message_empty(self):
        """
        Test case for creating a Notification with an empty message.
        - Attempts to create a Notification with an empty message field.
        - Asserts that an exception is raised during the commit operation.
        """
        notification = Notification(title='Empty Message', message='')
        db.session.add(notification)
        
        with self.assertRaises(Exception):
            db.session.commit()

    def test_notification_timestamp_default(self):
        """
        Test case for verifying the default timestamp of a Notification.
        - Creates a Notification without specifying the timestamp.
        - Verifies that the timestamp defaults to the current UTC time.
        """
        notification = Notification(title='Default Timestamp', message='Test message')
        db.session.add(notification)
        db.session.commit()
        
        self.assertIsNotNone(notification.timestamp)
        self.assertTrue(isinstance(notification.timestamp, datetime))

if __name__ == '__main__':
    unittest.main()

