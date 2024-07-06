from app import db
from sqlalchemy.sql import func

class Booking(db.Model):
    """Represents a booking made by a passenger."""
    __tablename__ = 'Booking'

    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('Passenger.id'), nullable=False)
    departure_place = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, default=func.now()) # 

    fare = db.Column(db.String(10, 2), nullable=False)

    # Relationship with Passenger
    passenger = db.relationship('Passenger', back_populates='bookings')

    def to_dict(self):
        """Converts the object to a dictionary representation."""
        return {
            'id': self.id,
            'passenger_id': self.passenger_id,
            'departure_place': self.departure_place,
            'destination': self.destination,
            'date_time': self.date_time.isoformat(),
            'fare': self.fare
        }

    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        """Returns a string representation of the Passenger object."""
        return f'<Booking {self.id}, {self.passenger_id}>'
