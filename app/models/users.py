from . import db
from flask_login import UserMixin
from . import login_manager

class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(16), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Returns a user object."""
        return f'<User {User.username}, {User.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
