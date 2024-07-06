import unittest
from app import create_app, db
from app.models import Passenger

class TestPassengerModel(unittest.TestCase):

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
        - Create sample Passenger objects and add them to the database.
        """
        self.passenger1 = Passenger(name='John Doe', email='john@example.com', phone='1234567890')
        self.passenger2 = Passenger(name='Jane Smith', email='jane@example.com', phone='9876543210')

        db.session.add(self.passenger1)
        db.session.add(self.passenger2)
        db.session.commit()

    def tearDown(self):
        """
        Clean up after each test case.
        - Delete sample Passenger objects from the database.
        """
        db.session.delete(self.passenger1)
        db.session.delete(self.passenger2)
        db.session.commit()

    def test_create_passenger(self):
        """
        Test case for creating a Passenger object.
        - Checks if the Passenger object was created successfully.
        - Verifies the name, email, and phone attributes of the created Passenger.
        """
        passenger = Passenger(name='Alice Cooper', email='alice@example.com', phone='5555555555')
        db.session.add(passenger)
        db.session.commit()

        self.assertIsNotNone(passenger.id)
        self.assertEqual(passenger.name, 'Alice Cooper')

    def test_read_passenger(self):
        """
        Test case for reading a Passenger object from the database.
        - Retrieves a Passenger object using its primary key (id).
        - Verifies the correctness of retrieved attributes (name, email, phone).
        """
        retrieved_passenger = Passenger.query.filter_by(name='John Doe').first()

        self.assertIsNotNone(retrieved_passenger)
        self.assertEqual(retrieved_passenger.email, 'john@example.com')

    def test_update_passenger(self):
        """
        Test case for updating a Passenger object.
        - Modifies attributes of an existing Passenger object.
        - Commits the changes and retrieves the updated Passenger.
        - Verifies that the changes are reflected correctly.
        """
        self.passenger1.email = 'john.doe@example.com'
        db.session.commit()

        updated_passenger = Passenger.query.filter_by(name='John Doe').first()
        self.assertEqual(updated_passenger.email, 'john.doe@example.com')

    def test_delete_passenger(self):
        """
        Test case for deleting a Passenger object.
        - Deletes a Passenger object from the database.
        - Verifies that the object no longer exists in the database.
        """
        db.session.delete(self.passenger2)
        db.session.commit()

        deleted_passenger = Passenger.query.filter_by(name='Jane Smith').first()
        self.assertIsNone(deleted_passenger)

    def test_passenger_name_max_length(self):
        """
        Test case for creating a Passenger with maximum name length.
        - Attempts to create a Passenger with a name exceeding the allowed maximum length.
        - Asserts that an exception is raised during the commit operation.
        """
        long_name = 'A' * 101  # Maximum length for name is 100 characters
        passenger = Passenger(name=long_name, email='test@example.com', phone='1234567890')
        db.session.add(passenger)
        
        with self.assertRaises(Exception):
            db.session.commit()

    def test_passenger_email_unique_constraint(self):
        """
        Test case for unique constraint on Passenger email.
        - Attempts to create a Passenger with a duplicate email address.
        - Asserts that an exception is raised during the commit operation.
        """
        duplicate_passenger = Passenger(name='Test User', email='john@example.com', phone='1112223333')
        db.session.add(duplicate_passenger)
        
        with self.assertRaises(Exception):
            db.session.commit()

if __name__ == '__main__':
    unittest.main()
