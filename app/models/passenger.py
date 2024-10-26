from . import db


class Passenger(db.Model):
    """ Passenger model class"""

    __tablename__ = 'passenger'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(16), unique=True, nullable=False)

    # Relationship with Booking
    passenger_bookings = db.relationship('PassengerBooking', backref='passenger', lazy=True)

    # __table_args__ = {'extend_existing': True}

    def to_dict(self):
        """
        Method to return  a dictionary representation of passenger object

        Returns:
        - dict: Dictionary containing
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone
        }
    
    def __repr__(self):
        """Returns a string representation of the passenger object"""
        return f'<Passenger {self.username}, {self.email}'