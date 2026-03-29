from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    """Represents an amenity available at a place (Wi-Fi, pool...)."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        """Name must not be empty and max 50 characters."""
        if not name or len(name) > 50:
            raise ValueError("Amenity name required, max 50 characters")
        return name

    def to_dict(self):
        """Converts the Amenity object into a dictionary."""
        base = super().to_dict()
        base.update({'name': self.name})
        return base