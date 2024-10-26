from sqlalchemy.sql import func
from . import db

class BaseBooking(db.Model):
    """Base class for common booking attributes"""
    __abstract__ = True  # Mark as an abstract class, no table created
    id = db.Column(db.Integer, primary_key=True)
    departure_place = db.Column(db.String(25), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    departure_date_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        """Converts the object to a dictionary representation"""
        return {
            'id': self.id,
            'departure_place': self.departure_place,
            'destination': self.destination,
            'departure_date_time': self.departure_date_time
        }

    def __repr__(self):
        """Returns a string representation of the object"""
        return f"<Booking {self.departure_place} to {self.destination} >"


class UserBooking(BaseBooking):
    """Represents a booking made by a registered user"""
    __tablename__ = 'user_booking'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        """Converts user object to dictionary"""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id
        })
        return data


class PassengerBooking(BaseBooking):
    """Represents a booking made by a guest user"""
    __tablename__ = 'passenger_booking'

    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.id'), nullable=False)

    def to_dict(self):
        """Converts the passenger object to a dictionary"""
        data = super().to_dict()
        data.update({
            'passenger_id': self.passenger_id
        })
        return data
