import unittest
from datetime import datetime
from app import db, Booking, Passenger

class TestBookingModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database for testing
        cls.db = db
        cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Remove the database tables after testing
        cls.db.drop_all()

    def test_booking_creation(self):
        # Create a sample Passenger
        passenger = Passenger(name='John Doe', email='john@example.com')
        self.db.session.add(passenger)
        self.db.session.commit()

        # Create a Booking instance
        booking = Booking(
            passenger_id=passenger.id,
            departure_place='City A',
            destination='City B',
            date_time=datetime.now(),
            fare=100.00
        )

        # Add Booking to session and commit
        self.db.session.add(booking)
        self.db.session.commit()

        # Retrieve the booking from the database
        retrieved_booking = Booking.query.filter_by(id=booking.id).first()

        # Assertions to check if the booking was created correctly
        self.assertIsNotNone(retrieved_booking)
        self.assertEqual(retrieved_booking.passenger_id, passenger.id)
        self.assertEqual(retrieved_booking.departure_place, 'City A')
        self.assertEqual(retrieved_booking.destination, 'City B')
        self.assertEqual(retrieved_booking.fare, 100.00)

    def test_booking_to_dict(self):
        # Create a sample Booking
        booking = Booking(
            passenger_id=1,
            departure_place='City A',
            destination='City B',
            date_time=datetime(2024, 7, 4, 10, 30),
            fare=80.50
        )

        # Convert Booking to dictionary
        booking_dict = booking.to_dict()

        # Assertions to check dictionary output
        self.assertEqual(booking_dict['passenger_id'], 1)
        self.assertEqual(booking_dict['departure_place'], 'City A')
        self.assertEqual(booking_dict['destination'], 'City B')
        self.assertEqual(booking_dict['date_time'], '2024-07-04T10:30:00')
        self.assertEqual(booking_dict['fare'], '80.50')

if __name__ == '__main__':
    unittest.main()
