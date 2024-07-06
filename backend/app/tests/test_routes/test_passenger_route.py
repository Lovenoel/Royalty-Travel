import unittest
import json
from app import create_app, db
from app.models import Passenger

class TestPassengerRoutes(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()
    
    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def test_get_all_passengers(self):
        # Add some test passengers to the database
        test_passengers = [
            Passenger(name='John Doe'),
            Passenger(name='Jane Smith')
        ]
        db.session.add_all(test_passengers)
        db.session.commit()

        # Make GET request to retrieve all passengers
        response = self.client.get('/passenger/passengers')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(data), 2)  # Expecting 2 passengers
        self.assertEqual(data[0]['name'], 'John Doe')
        self.assertEqual(data[1]['name'], 'Jane Smith')

    def test_create_passenger(self):
        # Data for creating a new passenger
        new_passenger_data = {
            'name': 'Alice Wonderland'
        }

        # Make POST request to create a new passenger
        response = self.client.post('/passenger/passengers', json=new_passenger_data)
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Alice Wonderland')

        # Check if the new passenger is actually added to the database
        created_passenger = Passenger.query.get(data['id'])
        self.assertIsNotNone(created_passenger)
        self.assertEqual(created_passenger.name, 'Alice Wonderland')

    def test_get_existing_passenger(self):
        # Add a test passenger to the database
        test_passenger = Passenger(name='Bob Builder')
        db.session.add(test_passenger)
        db.session.commit()

        # Make GET request to retrieve the added passenger
        response = self.client.get(f'/passenger/passenger/{test_passenger.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['name'], 'Bob Builder')

    def test_get_non_existing_passenger(self):
        # Make GET request for a non-existent passenger ID
        response = self.client.get('/passenger/passenger/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
