from . import db

class Bus(db.Model):
    """Represents a bus in the system"""
    __tablename__ = 'Bus'


    id = db.Column(db.Integer, primary_key=True)
    number_plate = db.Column(db.String(10), nullable=False, unique=True )
    capacity = db.Column(db.String(4), nullable=False)
    availability = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String(25), nullable=False)
    location = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        """Returns a string representation of the Bus object."""
        return f'<Bus {self.number_plate}, {self.model}, {self.capacity}, {self.location}>'
    

class Taxi(db.Model):
    """Represents a bus in the system"""
    __tablename__ = 'taxi'


    id = db.Column(db.Integer, primary_key=True)
    # number_plate = db.Column(db.String(50), nullable=False, unique=True )
    number_plate = db.Column(db.String(50), unique=True, nullable=True)
    capacity = db.Column(db.String(4), nullable=False)
    availability = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String(25), nullable=False)
    location = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        """Returns a string representation of the Bus object."""
        return f'<Bus {self.number_plate}, {self.model}, {self.capacity}, {self.location}>'
    