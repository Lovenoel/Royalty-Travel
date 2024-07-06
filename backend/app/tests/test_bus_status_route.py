import unittest
from app import create_app, db
from app.models import Bus, BusStatus

class TestBusRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.
        - Creates a Flask application instance for testing.
        - Sets up a test client to simulate requests.
        - Establishes an application context.
        - Creates all database tables.
        """
        cls.app = create_app('testing')  # Create a Flask application instance for testing
        cls.client = cls.app.test_client()  # Create a test client to simulate requests
        cls.ctx = cls.app.app_context()  # Establish an application context
        cls.ctx.push()
        db.create_all()  # Create all database tables
        cls.setup_test_data()  # Setup initial test data

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the test environment after all tests.
        - Removes the application context.
        - Drops all database tables.
        """
        db.session.remove()  # Remove the database session
        db.drop_all()  # Drop all database tables
        cls.ctx.pop()  # Remove the application context

    @classmethod
    def setup_test_data(cls):
        """
        Setup initial test data.
        - Creates sample bus data for testing.
        """
        # Create sample buses
        cls.bus1 = Bus(number_plate='ABC123', capacity=50, current_passenger_count=0, location='Area A')
        cls.bus2 = Bus(number_plate='XYZ789', capacity=40, current_passenger_count=30, location='Area B')
        db.session.add_all([cls.bus1, cls.bus2])  # Add sample buses to the database session
        db.session.commit()  # Commit changes to the database

    def test_enter_bus_success(self):
        """
        Test case for entering a bus with available capacity.
        """
        initial_passenger_count = self.bus1.current_passenger_count  # Record initial passenger count
        response = self.client.post(f'/bus_status/enter_bus/{self.bus1.id}')  # Send POST request to enter the bus
        self.assertEqual(response.status_code, 200)  # Assert HTTP status code is 200 (OK)
        self.assertEqual(self.bus1.current_passenger_count, initial_passenger_count + 1)  # Check passenger count incremented

    def test_enter_bus_full(self):
        """
        Test case for entering a bus that is already full.
        """
        response = self.client.post(f'/bus_status/enter_bus/{self.bus2.id}')  # Send POST request to enter the bus
        self.assertEqual(response.status_code, 400)  # Assert HTTP status code is 400 (Bad Request)
        self.assertIn('Bus is full', response.json['message'])  # Check for 'Bus is full' message in JSON response

    def test_enter_bus_not_found(self):
        """
        Test case for entering a bus that does not exist.
        """
        response = self.client.post('/bus_status/enter_bus/999')  # Send POST request to enter a non-existent bus
        self.assertEqual(response.status_code, 404)  # Assert HTTP status code is 404 (Not Found)
        self.assertIn('Bus not found', response.json['message'])  # Check for 'Bus not found' message in JSON response

    def test_buses_in_area(self):
        """
        Test case for retrieving buses in a specific area.
        """
        response = self.client.get('/bus_status/buses_in_area', query_string={'area': 'Area B'})  # Send GET request to retrieve buses in 'Area B'
        self.assertEqual(response.status_code, 200)  # Assert HTTP status code is 200 (OK)
        self.assertEqual(response.json['number_of_buses'], 1)  # Check number of buses returned is 1
        self.assertEqual(response.json['buses'][0]['number_plate'], 'XYZ789')  # Check the number plate of the bus returned

    def test_get_bus_status(self):
        """
        Test case for retrieving all bus statuses.
        """
        response = self.client.get('/bus_status/bus-status')  # Send GET request to retrieve all bus statuses
        self.assertEqual(response.status_code, 200)  # Assert HTTP status code is 200 (OK)
        self.assertEqual(len(response.json), 2)  # Check the number of buses returned matches the setup_test_data() count

if __name__ == '__main__':
    unittest.main()
