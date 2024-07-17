from app import db, bcrypt
from werkzeug.security import generate_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    SQLAlchemy model class representing users.

    Attributes:
    - id: Primary key for the User table.
    - username: Username of the user.
    - email: Email address of the user (unique).
    - password: Password hash of the user's password.
    - phone: Phone number of the user.

    Table Name:
    - __tablename__: Specifies the database table name for this model ('user').

    Usage:
    - This model facilitates storage and retrieval of user details within a database.
    - Implements password hashing and verification methods for secure password storage.

    Example:
    - Each record in this table represents a user with associated attributes such as username, email, password hash, and phone number.

    Notes:
    - Adjust `username`, `email`, `password`, and `phone` attributes as per specific application requirements.
    """

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15))
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship with Booking
    bookings =db.relationship('UserBooking', back_populates='user', overlaps="bookings", lazy=True)

    def __repr__(self):
        """
        Method to return a string representation of the User object.

        Returns:
        - str: String representation indicating the username, email, and phone of the User.
        """
        return f'<User {self.username}, {self.email}, {self.phone}>'

    def set_password(self, password):
        """
        Method to set the password for the User.

        Args:
        - password: Plain text password to be hashed and stored securely.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Method to check if the provided password matches the stored password hash.

        Args:
        - password: Plain text password to be checked against the stored hash.

        Returns:
        - bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)
