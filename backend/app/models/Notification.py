from app import db
from sqlalchemy.sql import func


class Notification(db.Model):
    """
    SQLAlchemy model class representing notifications.

    Attributes:
    - id: Primary key for the Notification table.
    - title: Title of the notification.
    - message: Content of the notification message.
    - timestamp: Timestamp indicating when the notification was created.
    - read: Shows whether it's been read or not

    Table Name:
    - __tablename__: Specifies the database table name for this model ('Notification').

    Table Arguments:
    - __table_args__: Allows extending existing table schema if it already exists in the database.

    Usage:
    - This model facilitates storage and retrieval of notification details within a database.
    - Suitable for use with SQLAlchemy ORM in Flask applications for managing notification data.

    Example:
    - Each record in this table represents a notification with a unique title, message, and creation timestamp.

    Notes:
    - Adjust `title`, `message`, and `timestamp` attributes as per specific application requirements.
    """

    __tablename__ = 'Notification'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    read = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Converts a notification object to a dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'timestamp': self.timestamp,
            'read': self.read
        }


    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        """Returns a string representation  a notification object"""
        return f'<Notification {self.id}, {self.title}, {self.message}, {self.timestamp}>'
