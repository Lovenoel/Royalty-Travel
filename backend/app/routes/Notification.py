from flask import Blueprint, render_template
from app import db
from app.models.Notification import Notification

notification_bp = Blueprint('notifications', __name__, url_prefix='/notification')

@notification_bp.route('/notifications')
def notifications():
    notifications = Notification.query.order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=notifications)

