```mermaid
sequenceDiagram

participant Client as User (Client)
participant API as API/Facade
participant User as User Entity
participant Place as Place Entity 
participant Amenity as Amenity Entity
participant BaseModel as BaseModel 
participant DB as Database 

Client->>API: POST /places (token, name, description, price, latitude, longitude, amenities)
API->>API: Extract user_id from token

API->>User: verify_password(token) 
User-->>API: Authenticated (user_id)

API->>Place: create new Place instance 
Place->>BaseModel: Generate UUID (id) 
Place->>BaseModel: Set created_at, updated_at 
Place->>Place: Set owner_id = user_id

Place->>Place: set_price(price) 
Place->>Place: Validate latitude, longitude

loop For each amenity 
   Place->>Place: add_amenity(amenity) 
   Place->>Amenity: Create relationship 
end

Place->>BaseModel: save() 
BaseModel->>DB: INSERT place 
DB-->>BaseModel: Success 

BaseModel->>BaseModel: to_dict() 
BaseModel-->>API: Place data (dict) 
API-->>Client: 201 Created (place_data) 