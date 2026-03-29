from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates

#  Many-to-many Place association table ↔ Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)
class Place(BaseModel):
    """
    Represents a property or location in the system.
    Manages location information, pricing, and relationships with reviews and amenities.
    
    """
    __tablename__ = 'places'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # Foreign key to the User
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    owner     = db.relationship('User', backref=db.backref('places', lazy=True))
    reviews   = db.relationship('Review', backref=db.backref('place', lazy=True))
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))
    
    @validates('price')
    def validate_price(self, key, price):
        """Validates that the price is a positive number."""
        if price < 0:
            raise ValueError("Price must be positive")
        return price
    
    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Validates that the longitude is between -180 and 180."""
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return longitude

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Validates that the latitude is between -90 and 90."""
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return latitude
    
    def to_dict(self):
        """
        Converts the Place object and its relationships into a dictionary.
        
        Returns:
            dict:  Complete location details including owner ID and amenities.
        """
        base = super().to_dict()
        base.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': [a.to_dict() for a in self.amenities]
        })
        return base