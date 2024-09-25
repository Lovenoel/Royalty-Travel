from . import db

class Receipt(db.Model):
    """
    SQLAlchemy model class representing receipts.

    Attributes:
    - id: Primary key for the Receipt table.
    - username: Name of the passenger
    - booking_id: Foreign key reference to the Booking table.
    - amount: Amount paid for the booking.

    Table Name:
    - __tablename__: Specifies the database table name for this model ('Receipt').

    Usage:
    - This model facilitates storage and retrieval of receipt details within a database.
    - Suitable for use with SQLAlchemy ORM in Flask applications for managing payment receipts.

    Example:
    - Each record in this table represents a receipt associated with a booking, detailing the amount paid.
    """

    __tablename__ = 'Receipt'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    booking_id = db.Column(db.Integer)
    amount = db.Column(db.Float)

    __table_args__ = {'extend_existing': True}

    def to_dict(self):
        """
        Method to return a dictionary representation of the Receipt object.

        Returns:
        - dict: Dictionary containing id, username, booking_id, and amount attributes of the Receipt.
        """
        return {
            'id': self.id,
            'username': self.username,
            'booking_id': self.booking_id,
            'amount': self.amount
        }

    def __repr__(self):
        """
        Method to return a string representation of the Receipt object.

        Returns:
        - str: String representation indicating the id of the Receipt.
        """
        return f'<Receipt {self.id}>'
