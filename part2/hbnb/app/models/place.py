from app.models.base_model import BaseModel
from app import db
from sqlalchemy.orm import validates

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

    def set_price(self, price):
        """
        Sets the price after validation. 
        
        Raises:
            ValueError: if the price is negative.
        """
        if price < 0:
            raise ValueError("Price must be positive")
        self._price = price

    def get_price(self):
        """Returns the actual price of the place."""
        return self._price

    def _validate_coordinates(self, latitude, longitude):
        """
        Internal method to validate GPS coordinates.
        
        Raises:
            ValueError: If the latitude or longitude are out of bounds.
        """
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._latitude = latitude
        self._longitude = longitude

    def is_available(self):
        """Checks if the place is available for booking ( Default True )."""
        return True

    def add_amenity(self, amenity):
        """
        Adds an amenity to the place if it is not already present.
        
        Args:
            amenity (Amenity): The amenity object to add.
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Deletes an amenity from the place if it exists."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def add_review(self, review):
        """Add a customer review to the list of reviews for this place."""
        self.reviews.append(review)

    def get_average_rating(self):
        """
        Calculates the average rating for this place.
        
        Returns:
            float: Average rating or 0.0 if no reviews exist.
        """
        if not self.reviews:
            return 0.0
        return sum(r.rating for r in self.reviews) / len(self.reviews)

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
            'price': self._price,
            'latitude': self._latitude,
            'longitude': self._longitude,
            'owner_id': self.owner.id,
            'amenities': [a.to_dict() for a in self.amenities]
        })
        return base