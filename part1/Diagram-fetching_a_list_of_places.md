```mermaid
sequenceDiagram
autonumber
    participant Client as User (client)
    participant API as API/Facade(PersistenceLayer)
    participant Place as Place Entity (BusinessLogicLayer)
    participant Review as Review Entity (BusinessLogicLayer)
    participant Amenity as Amenity Entity (BusinessLogicLayer)
    participant BaseModel as BaseModel (BusinessLogicLayer)
    participant DB as Database(PersistenceLayer)

    Client->>API: GET /places?max_price=250&amenities=Pool
    API->>API: Parse query parameters
    
    API->>Place: Build filters (max_price, amenities)
    Place->>DB: SELECT places WHERE criteria
    DB-->>Place: List of places
    
    loop For each place
        Place->>Place: is_available()
        
        alt Place is available
            Place->>Place: get_price()
            Place->>Place: get_average_rating()
            
            Place->>Review: list_by_place(place_id)
            Review->>DB: Get reviews for place
            DB-->>Review: Reviews list
            
            Place->>Amenity: Get amenities for place
            Amenity->>DB: Get amenities
            DB-->>Amenity: Amenities list
            
            Place->>BaseModel: to_dict()
            BaseModel-->>Place: Place dict with reviews and amenities
        end
    end
    
    Place-->>API: List of places (formatted)
    API-->>Client: 200 OK (places_list)
