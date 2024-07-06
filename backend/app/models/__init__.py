from app import db

from .Passenger import Passenger
from .Booking import Booking
from .Bus import Bus
from .Notification import Notification
from .BusStatus import BusStatus
from .Receipt import Receipt
from .User import User

__all__ = ['Passenger', 'Booking', 'Bus', 'Notification', 'BusStatus', 'Receipt', 'User']
