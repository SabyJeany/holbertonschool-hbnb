from app.models.base_model import BaseModel

class Review(BaseModel):
    """
    Represents a review left by a user for a specific place. 
    including a textual comment and a rating between 1 and 5.
    
    """
    def __init__(self, text, rating, place, user):
        """Initializes a new review.

        Args:
            text (str): The content of the review.
            rating (int): The rating given, must be (between 1 and 5).
            place (Place): The instance of the place.
            user (User): The instance of the user who wrote the review.
        """
        super().__init__()
        self.text = text
        self._rating = None
        self.place = place
        self.user = user
        self.rating = rating

    @property
    def rating(self):
        """Returns the rating of the review."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """ 
        Defines the rating value with validation.
        Raises:
            ValueError: If the rating is not between 1 and 5.
        """
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value

    @staticmethod
    def list_by_place(reviews, place_id):
        """
        Filters a list of reviews to return only those that match the specified place ID.
         Args:
            reviews (list): A completed list of review objects.
            place_id (str): The ID of the place to filter by.

            Returns:
                list: A list of reviews that belong to the specified place.
            """
        return [r for r in reviews if r.place.id == place_id]

    @staticmethod
    def list_by_user(reviews, user_id):
        """ Filters a list of reviews to return only those that match the specified user ID.
         Args:
            reviews (list): A completed list of review objects.
            user_id (str): The ID of the user to filter by.

            Returns:
                list: A list of reviews that belong to the specified user.
            """
        return [r for r in reviews if r.user.id == user_id]

    def to_dict(self):
        """ 
        Converts the Review object and its relationships into a dictionary.
        Include the idof the relatiosnships (place_id and user_id).
        """
        base = super().to_dict()
        base.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id
        })
        return base