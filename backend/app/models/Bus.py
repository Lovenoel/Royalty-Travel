from app import db

class Bus(db.Model):
    """Represents a bus in the system."""
    __tablename__ = 'Bus'

    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_passenger_count = db.Column(db.Integer, default=0)
    location = db.Column(db.String(100), nullable=True)

    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        """Returns a string representation of the Bus object."""
        return f'<Bus {self.number_plate}, {self.capacity}, {self.location}>'

    
