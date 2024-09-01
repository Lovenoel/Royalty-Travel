from app import db

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
__all__ = ['Passenger', 'UserBooking', 'PassengerBooking', 'Bus', 'Notification', 'BusStatus', 'Receipt', 'User', 'Post']
