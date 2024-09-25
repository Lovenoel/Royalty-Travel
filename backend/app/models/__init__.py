from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

# Import models from models
from .Passenger import Passenger
from .Booking import UserBooking, PassengerBooking
from .Bus import Bus
from .Notification import Notification
from .BusStatus import BusStatus
from .Receipt import Receipt
from .User import User
from .Post import Post

# Make the models available to the all application
__all__ = ['db', 'bcrypt', 'Passenger', 'UserBooking', 'PassengerBooking', 'Bus', 'Notification', 'BusStatus', 'Receipt', 'User', 'Post']
