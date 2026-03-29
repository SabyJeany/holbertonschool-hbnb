from app import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
import re

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean, default=False)

    @validates('email')
    def validate_email(self, key, email):
        """Validates email format before storing."""
        regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex_email, email):
            raise ValueError(f"Invalid email: {email}")
        return email

    def hash_password(self, password):
        """Hash the password before storing it."""
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def get_average_rating(self, reviews):
        """Calculate the average rating from a list of reviews."""
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