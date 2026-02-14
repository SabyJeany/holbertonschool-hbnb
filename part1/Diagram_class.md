```mermaid
---
config:
  theme: Neo Dark
  look: Neo
---
classDiagram

direction TB
    class BaseModel {
	    + id : UUID4 
	    + created_at : string
	    + updated_at : string
	    + save()
        + delete()
        + updated()
        + to_dict()

    }
    
    class User {
        - email : string
        - password : string
        + first_name : string 
        + last_name: string
        - is_admin: boolean
        + hash_password()
        + verify_password()
        - verify_password()
        -verify_email()
        +get_average_rating()

        
    }
    
    class Place {
        - owner_id: UUID4
        + name : string 
        + description: string
        + price : float
        + latidute : float
        + longitude : float
        + get_price()
        + set_price() 
        + is_available()
        + add_amenity()
        + remove_amenity()
        + get_average_rating()
    }
    
    class Review {+ place_id : UUID4
    + user_id : UUID4
    + rating: integrer
    +comments : string
    list_by_place()
    list_by_user()
    }

    class Amenity {-description : string
    -name : string}

    BaseModel <|-- User : inherits
    BaseModel <|-- Place : inherits
    BaseModel <|-- Review: inherits
    BaseModel <|-- Amenity : inherints

    User "1" --> "*" Place : owns
    User "1" --> "*" Review : can writes
    Place "1" --> "*" Amenity : has
    Place "1" --> "*" Review : receives multiple