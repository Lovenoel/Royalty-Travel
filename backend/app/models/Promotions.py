from . import db

class Promotion(db.Model):
    """A class model for Promotions """

    __tablename__ = 'Promotions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        """
        Method that returns a dictionary representation of a Promotion object

        Returns:
        - dict: Dictionary containing id, title, description attributes of Promotion
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

    def __repr__(self):
        return f"Promotion('{self.title}', '{self.description}')"
