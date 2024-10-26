from . import db
from flask_login import UserMixin
from . import login_manager

class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(16), nullable=False, unique=True)
    # profile_picture = db.Column(db.String(100))
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    user_bookings = db.relationship('UserBooking', backref='user', lazy=True)

    def __repr__(self):
        """Returns a user object."""
        return f'<User {self.username}, {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
