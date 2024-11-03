from . import db


class Post(db.Model):
    """Post class model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_public = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    author = db.relationship('User', backref=db.backref('posts', lazy=True))


    def __repr__(self):
        return f"<Post {self.title}>"