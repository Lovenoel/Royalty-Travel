'''Booking Service
Handles the Booking Process
- Creates new bookings
- Gets a booking by it's booking_id
'''
from app.models import Booking


class BookingService:
    def __init__(self, db):
        """Intializes the database
            Args:
                db - database
        """
        self.db = db

    def create_booking(self, passenger_name, departure, destination, datetime):
        """ Creates a new booking
        Args:
            passenger_name(str):
            departure(str):
            destination(str):
            travel_datetime(int):
        Returns:
            a new booking.
        """
        new_booking = Booking(
            passenger_name=passenger_name,
            departure=departure,
            destination=destination,
            travel_datetime=datetime
        )
        self.db.session.add(new_booking)
        self.db.session.commit()
        return new_booking


    def get_bookings(self):
        """Gets a booking from the database
            Returns:
                a booking.
        """
        return Booking.query.all()

    def get_booking_by_id(self, booking_id):
        """Gets a booking by it's booking ID
        Args:
            booking_id(int):
        Rturns:
            a booking once found in the database
            None if not found
        """
        return Booking.query.get(booking_id)
