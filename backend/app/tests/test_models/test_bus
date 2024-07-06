import unittest
from app import create_app, db
from app.models import Bus

class TestBusModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a test Flask application
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up after all tests
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def setUp(self):
        # Create a sample bus for each test
        self.bus = Bus(
            number_plate='ABC123',
            capacity=50,
            current_passenger_count=0,
            location='City A'
        )
        db.session.add(self.bus)
        db.session.commit()

    def tearDown(self):
        # Remove the bus object after each test
        db.session.delete(self.bus)
        db.session.commit()

    def test_bus_creation(self):
        # Test if the bus object was created successfully
        bus = Bus.query.filter_by(number_plate='ABC123').first()
        self.assertIsNotNone(bus)
        self.assertEqual(bus.capacity, 50)
        self.assertEqual(bus.current_passenger_count, 0)
        self.assertEqual(bus.location, 'City A')

    def test_bus_retrieval(self):
        # Test retrieving the bus object from the database
        bus = Bus.query.filter_by(number_plate='ABC123').first()
        self.assertIsNotNone(bus)
        self.assertEqual(bus.capacity, 50)
        self.assertEqual(bus.current_passenger_count, 0)
        self.assertEqual(bus.location, 'City A')

    def test_bus_update(self):
        # Test updating the bus object
        self.bus.capacity = 60
        self.bus.location = 'City B'
        db.session.commit()
        
        updated_bus = Bus.query.filter_by(number_plate='ABC123').first()
        self.assertEqual(updated_bus.capacity, 60)
        self.assertEqual(updated_bus.location, 'City B')

    def test_bus_deletion(self):
        # Test deleting the bus object
        db.session.delete(self.bus)
        db.session.commit()
        
        deleted_bus = Bus.query.filter_by(number_plate='ABC123').first()
        self.assertIsNone(deleted_bus)

if __name__ == '__main__':
    unittest.main()
