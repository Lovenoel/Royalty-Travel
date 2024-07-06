from datetime import datetime, timedelta, timezone
from app.models import Booking, Notification

def check_and_send_notifications():
    now = datetime.now(timezone.utc)
    bookings = Booking.query.all()
    
    for booking in bookings:
        time_until_departure = booking.departure_time - now
        if time_until_departure <= timedelta(minutes=30) and time_until_departure > timedelta(minutes=29):
            send_notification(booking, "Bus is 30 minutes away", "Your bus is 30 minutes away from the departure location.")
        elif time_until_departure <= timedelta(minutes=15) and time_until_departure > timedelta(minutes=14):
            send_notification(booking, "Bus is 15 minutes away", "Your bus is 15 minutes away from the departure location.")

def send_notification(booking, title, message):
    from app import db
    notification = Notification(
        booking_id=booking.id,
        title=title,
        message=message
    )
    db.session.add(notification)
    db.session.commit()
