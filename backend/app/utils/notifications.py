from datetime import datetime, timedelta, timezone
from ..models import UserBooking, PassengerBooking, Notification

def check_and_send_notifications():
    """
    Check all bookings and send notifications based on the time until departure.
    This function processes both user bookings and passenger bookings separately.
    """
    now = datetime.now(timezone.utc)  # Get the current time in UTC
    
    # Process notifications for registered users
    user_bookings = UserBooking.query.all()  # Get all user bookings from the database
    process_notifications(user_bookings, now)  # Process notifications for user bookings
    
    # Process notifications for passengers
    passenger_bookings = PassengerBooking.query.all()  # Get all passenger bookings from the database
    process_notifications(passenger_bookings, now)

def process_notifications(bookings, now):
    """
    Process notifications for a list of bookings.
    
    :param bookings: List of booking objects to process
    :param now: Current datetime in UTC
    """
    for booking in bookings:
        time_until_departure = booking.departure_time - now  # Calculate time until departure
        
        # Check if the bus is 30 minutes away
        if time_until_departure <= timedelta(minutes=30) and time_until_departure > timedelta(minutes=29):
            send_notification(booking, "Bus is 30 minutes away", "Your bus is 30 minutes away from the departure location.")
        # Check if the bus is 15 minutes away
        elif time_until_departure <= timedelta(minutes=15) and time_until_departure > timedelta(minutes=14):
            send_notification(booking, "Bus is 15 minutes away", "Your bus is 15 minutes away from the departure location.")

def send_notification(booking, title, message):
    """
    Send a notification for a booking.
    
    :param booking: The booking object for which the notification is to be sent
    :param title: The title of the notification
    :param message: The message content of the notification
    """
    from app import db  # Import db object for database operations
    
    # Create a new Notification object with the given details
    notification = Notification(
        booking_id=booking.id,
        title=title,
        message=message
    )
    
    db.session.add(notification)  # Add the notification to the session
    db.session.commit()  # Commit the session to save the notification to the database
