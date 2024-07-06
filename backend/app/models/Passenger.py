from app import db

class Passenger(db.Model):
    """
    SQLAlchemy model class representing passengers.

    Attributes:
    - id: Primary key for the Passenger table.
    - username: Name of the passenger.
    - email: Email address of the passenger.
    - phone: Phone number of the passenger.

    Relationships:
    - bookings: One-to-many relationship with Booking model, representing bookings made by the passenger.

    Table Name:
    - __tablename__: Specifies the database table name for this model ('Passenger').

    Table Arguments:
    - __table_args__: Allows extending existing table schema if it already exists in the database.

    Usage:
    - This model facilitates storage and retrieval of passenger details within a database.
    - Suitable for use with SQLAlchemy ORM in Flask applications for managing passenger data.

    Example:
    - Each record in this table represents a passenger with a unique name, email, and phone number.
    """

    __tablename__ = 'Passenger'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    # Relationship with Booking
    bookings = db.relationship('Booking', back_populates='passenger', lazy=True)

    __table_args__ = {'extend_existing': True}

    def to_dict(self):
        """
        Method to return a dictionary representation of the Passenger object.

        Returns:
        - dict: Dictionary containing id, username, email, and phone attributes of the Passenger.
        """
        return {
            'id': self.id,
            'name': self.username,
            'email': self.email,
            'phone': self.phone
        }

    def __repr__(self):
        """
        Method to return a string representation of the Passenger object.

        Returns:
        - str: String representation indicating the name of the Passenger.
        """
        return f'<Passenger {self.id}, {self.username}, {self.email}>'
