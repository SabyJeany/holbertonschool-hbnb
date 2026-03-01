from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """
    Facade class that bridges the presentation layer (API) with the business logic 
    and persistence layers. It centralizes all operations for the HBnB application.
    """

    def __init__(self):
        """
        Initializes the in-memory repositories for each entity type.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Creates and persists a new User instance.
        
        Args:
            user_data (dict): Dictionary containing user attributes (email, name, etc.).
        Returns:
            User: The newly created User object.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieves a user by their unique ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieves a user by their email address."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Returns a list of all registered users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Updates an existing user's information."""
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    def create_amenity(self, amenity_data):
        """Creates and persists a new Amenity instance."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its unique ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Returns a list of all available amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an existing amenity's information."""
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def create_place(self, place_data):
        """
        Creates a new Place after validating the existence of the owner.
        
        Args:
            place_data (dict): Data for the place, including 'owner_id'.
        Raises:
            ValueError: If the specified owner_id does not exist.
        Returns:
            Place: The newly created Place object.
        """
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by its unique ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Returns a list of all registered places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Updates an existing place's information."""
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)
    
    def create_review(self, review_data):
        """
        Creates a new Review by linking a User and a Place.
        
        Args:
            review_data (dict): Data including 'user_id', 'place_id', 'text', and 'rating'.
        Raises:
            ValueError: If the user or the place does not exist.
        Returns:
            Review: The newly created Review object.
        """
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        """Retrieves a specific review by its ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Returns all reviews across the platform."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Filters reviews to return only those linked to a specific place."""
        return [r for r in self.review_repo.get_all() if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        """Updates an existing review's text or rating."""
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Removes a review from the repository."""
        self.review_repo.delete(review_id)