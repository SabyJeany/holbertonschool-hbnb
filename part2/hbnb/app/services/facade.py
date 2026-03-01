from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    """
    Implementations of the facade pattern to centralize the business logic .
    This class provides a abstraction layer between the presentaion layer (API/UI) and the persistence layer.
    it coordinates operations on the repositories to ensure data integrity and consistency across the application.
    """
    def __init__(self):
        """
        Initialize the instance of the repositories for each entity (User, Place, Review, Amenity).
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Creates a new user with the provided data and adds it to the user repository."""
        pass

    def get_place(self, place_id):
        """retrieves a entity 'Place' from the persistence layer.
        Args:
            place_id (str): The unique identifier of the place to retrieve.

        Returns:
                Place: the object representing the place with the given ID or None if not found.
        """
        pass