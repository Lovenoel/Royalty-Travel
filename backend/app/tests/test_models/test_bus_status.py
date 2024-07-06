import unittest
from app import create_app, db
from app.models import BusStatus

class TestBusStatusModel(unittest.TestCase):

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
        - Create a sample BusStatus object and add it to the database.
        """
        self.bus_status = BusStatus(
            bus_number='BUS001',
            status='On-time'
        )
        db.session.add(self.bus_status)
        db.session.commit()

    def tearDown(self):
        """
        Clean up after each test case.
        - Delete the sample BusStatus object from the database.
        """
        db.session.delete(self.bus_status)
        db.session.commit()

    def test_create_bus_status(self):
        """
        Test case for creating a BusStatus object.
        - Checks if the BusStatus object was created successfully.
        - Verifies the status attribute of the created BusStatus.
        """
        bus_status = BusStatus.query.filter_by(bus_number='BUS001').first()
        self.assertIsNotNone(bus_status)
        self.assertEqual(bus_status.status, 'On-time')

    def test_update_bus_status(self):
        """
        Test case for updating a BusStatus object.
        - Modifies the status attribute of the BusStatus object.
        - Asserts that the updated status matches the expected value.
        """
        self.bus_status.status = 'Delayed'
        db.session.commit()
        
        updated_bus_status = BusStatus.query.filter_by(bus_number='BUS001').first()
        self.assertEqual(updated_bus_status.status, 'Delayed')

    def test_delete_bus_status(self):
        """
        Test case for deleting a BusStatus object.
        - Deletes the BusStatus object from the database.
        - Checks if the BusStatus object no longer exists in the database.
        """
        db.session.delete(self.bus_status)
        db.session.commit()
        
        deleted_bus_status = BusStatus.query.filter_by(bus_number='BUS001').first()
        self.assertIsNone(deleted_bus_status)

    def test_get_bus_status(self):
        """
        Test case for retrieving a BusStatus object.
        - Retrieves the BusStatus object from the database.
        - Verifies the status attribute of the retrieved BusStatus.
        """
        retrieved_bus_status = BusStatus.query.filter_by(bus_number='BUS001').first()
        self.assertEqual(retrieved_bus_status.status, 'On-time')

    def test_invalid_bus_status_creation(self):
        """
        Test case for creating an invalid BusStatus object.
        - Attempts to create a BusStatus object with missing required fields.
        - Asserts that an exception is raised during commit.
        """
        invalid_bus_status = BusStatus(bus_number='BUS002')
        db.session.add(invalid_bus_status)
        
        with self.assertRaises(Exception):
            db.session.commit()

if __name__ == '__main__':
    unittest.main()
