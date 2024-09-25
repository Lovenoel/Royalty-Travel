from . import db
from sqlalchemy.sql import func
from app.models.Passenger import Passenger
from app.models.User import User

class BaseBooking(db.Model):
    """Base class for common booking attributes."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    departure_place = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, default=func.now())
    fare = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        """Converts the object to a dictionary representation."""
        return {
            'id': self.id,
            'departure_place': self.departure_place,
            'destination': self.destination,
            'date_time': self.date_time.isoformat(),
            'fare': self.fare
        }

    def __repr__(self):
        """Returns a string representation of the object."""
        return f'<Booking {self.id}, {self.departure_place} to {self.destination}>'


class UserBooking(BaseBooking):
    """Represents a booking made by a registered user."""
    __tablename__ = 'user_booking'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)

    # 
    def to_dict(self):
        """Converts the user object to a dictionary representation."""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'username': self.username,})
        return data
    
    __table_args__ = {'extend_existing': True}

class PassengerBooking(BaseBooking):
    """Represents a booking made by a passenger who is not a registered user."""
    __tablename__ = 'passenger_booking'

    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.id'), nullable=False)
    passenger_name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        """Converts the passenger object to a dictionary representation."""
        data = super().to_dict()
        data.update({
            'passenger_id': self.passenger_id,
            'passenger_name': self.passenger_name})
        return data
    
    __table_args__ = {'extend_existing': True}

    """def __repr__(self):
        "Returns a string representation of the Passenger object."
        return f'<Passengerbooking {self.id}, passenger_id={self.passenger_id}>'
    """
    