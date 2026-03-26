from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates


class Review(BaseModel):
    """
    Represents a review left by a user for a specific place. 
    including a textual comment and a rating between 1 and 5.
    
    """
    __tablename__ = 'reviews'
    text = db.Column(db.String(500), nullable=False)
    _rating = db.Column(db.Integer, nullable=False)

    # Foreign keys
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id  = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    @validates('_rating')
    def validate_rating(self, key, rating):
        """Validates that the rating is an integer between 1 and 5."""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def to_dict(self):
        """ 
        Converts the Review object and its relationships into a dictionary.
        Include the idof the relatiosnships (place_id and user_id).
        """
        base = super().to_dict()
        base.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
         })
        return base