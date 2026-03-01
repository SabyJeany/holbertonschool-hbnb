from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """
    Represents an amenity or an service available at a place, such as (Wi-Fi, pool).
    """
    def __init__(self, name: str):
        """
        Initializes a new amenity.
        Args:
            name (str): The name of the amenity, (ex: "Wifi").
        """
        super().__init__()
        self._name = None
        self.name = name

    @property
    def name(self):
        """Returns the name of the amenity."""
        return self._name
    
    @name.setter
    def name(self,name):
        """defines the name of the amenity with validation.
        Raises:
            ValueError: If the name is empty or exceeds 50 characters.
        """
        if not name or len(name) > 50:
            raise ValueError("Amenity name required, max 50 characters")
        self._name = name

    def to_dict(self):
        """Converts the Amenity object into a dictionary format."""
        base = super().to_dict()
        base.update({'name': self.name})
        return base