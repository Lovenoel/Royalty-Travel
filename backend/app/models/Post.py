from app import db
from sqlalchemy.sql import func

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=func.now() )
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        """
        Method to return a string representation of the Post object.

        Returns:
        - str: String representation indicating the title and date_posted
        """
        return f'<Post {self.title}, {self.date_posted}>'