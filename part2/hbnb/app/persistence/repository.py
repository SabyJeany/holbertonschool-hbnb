from abc import ABC, abstractmethod

class Repository(ABC):
    """
    This is a mandatory model that lists basic actions (add, search, delete). 
    It serves as a rule: any storage system created later must have these functions.
    """
    @abstractmethod
    def add(self, obj):
        """Adds a new object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieves an object by its ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieves a list of all objects in the repository."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Updates an existing object."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Deletes an object via its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieves an object based on a specific attribute."""
        pass


class InMemoryRepository(Repository):
    """ 
    Implementations of the repository storing data in memory using a dictionary. 
    Ideal for development and testing without requiring a database.
    """
    def __init__(self):
        """Initializes an empty dictionary to use as temporary storage."""
        self._storage = {}

    def add(self, obj):
        """Adds an object to the repository, using its ID as the key."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Returns the object associated with the given ID, or None if not found."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Returns a list of all objects currently stored in the repository."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Updates an existing object with new data provided in a dictionary format.
        The object requires an 'update' method to process the data.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Removes an object from the storage dictionary."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)