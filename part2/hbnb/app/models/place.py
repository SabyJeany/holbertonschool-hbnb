from app.models.base_model import BaseModel

class Place(BaseModel):
    """
    Represents a property or location in the system.
    Manages location information, pricing, and relationships with reviews and amenities.
    
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialises a new location.
        
        Args:
            title (str): Title of the listing.
            description (str): Detailed description.
            price (float): Price per night.
            latitude (float): Geographic latitude.
            longitude (float): Geographic longitude.
            owner (User): Instance of the user who owns the location.
        """
        super().__init__()
        self.title = title
        self.description = description
        self._price = None
        self._latitude = None
        self._longitude = None
        self.owner = owner
        self.reviews = []       
        self.amenities = []
        self.set_price(price)
        self._validate_coordinates(latitude, longitude)

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