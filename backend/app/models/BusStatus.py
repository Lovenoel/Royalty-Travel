from . import db
from datetime import datetime, timezone

class BusStatus(db.Model):
    """
    SQLAlchemy model class representing bus status information.

    Attributes:
    - id: Primary key for the BusStatus table.
    - bus_number: Bus identifier (e.g., bus number or code).
    - status: Current status of the bus (e.g., 'On-time', 'Delayed').

    Table Name:
    - __tablename__: Specifies the database table name for this model ('BusStatus').

    Table Arguments:
    - __table_args__: Allows extending existing table schema if it already exists in the database.

    Usage:
    - This model facilitates storage and retrieval of bus status information within a database.
    - Intended for use with SQLAlchemy ORM in Flask applications.
    """

    __tablename__ = 'BusStatus'

    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        """Returns a string representation of a BusStatus object"""
        return f'<BusStatus {self.id}, {self.bus_number}, {self.status}>'
