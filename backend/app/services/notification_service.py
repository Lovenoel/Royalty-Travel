"""
This is the Notification Service
Handles;
- Creation of a notification
- Get's a notification
- Marks a notification once it's read
"""


class NotificationService:
    """Intializes the database
    Args:
        db: the database
    """
    def __init__(self, db):
        self.db = db

    def create_notification(self, message, recipient):
        """ Creates a notification
        Args:
            message(str): Notification message
            recipient(str): Receiver of the message,
        Returns:
            a new notification,
            status: unread
        """
        new_notification = {
            "message": message,
            "recipient": recipient,
            "status": "unread"
        }
        self.db["notifications"].append(new_notification)
        return new_notification

    def get_notifications(self, recipient):
        """Returns notifications
        Args:
            recipient(str): receiver of the notification
        """
        return [n for n in self.db["notifications"] if n["recipient"] == recipient]

    def mark_as_read(self, notification_id):
        """ Returns notification 
        Args:
            notification_id: unique ID of a notification
        Returns:
            notification with status read once it's read
        """
        for notification in self.db["notifications"]:
            if notification["id"] == notification_id:
                notification["status"] = "read"
                return notification
        return None
