import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self._email = None
        self._password = None
        self._is_admin = is_admin
        self.verify_email(email)
        self.hash_password(password)

    def verify_email(self, email):
        """ Check that the email is correctly formatted according to the regex, and if it is, save it in _email.
    Args: 
    - email (str): The email address to validate.
    Raises:
    - ValueError: If the email format is not invalid."""
        
        regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex_email, email):
            raise ValueError(f"Invalid email: {email}")
        self._email = email

    @property
    def email(self):
        return self._email

    def hash_password(self, password):
        """
        checks the strength of the password and prepares it for hashing.
        Raises:
            ValueError: If the password is less than 6 characters long.
        """
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self._password = password

    def verify_password(self, password):
        """ 
        Compares the provided password with the stored password. 
        Returns:
            bool: True if they match, False otherwise.
        """
        return self._password == password

    @property
    def is_admin(self):
        """ indicates whether the user has administrative privileges. """
        return self._is_admin

    def get_average_rating(self, reviews):
        """
        Calculate the average rating from a list of reviews.
        Args:            reviews (list): A list of review objects, containing a 'rating' attribute.
        Returns:
            float: The average rating, or 0.0 if the list is empty.
        """
        if not reviews:
            return 0.0
        return sum(r.rating for r in reviews) / len(reviews)

    def to_dict(self):
        """Converts the User object into a dictionary for export (JSON/API)."""
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return base