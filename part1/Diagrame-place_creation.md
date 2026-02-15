```mermaid
sequenceDiagram
autonumber

participant Client as User 
participant API as API/Facade (PrésentationLayer)
participant User as User Entity (BusinessLogicLayer)
participant Place as Place Entity (BusinessLogicLayer)
participant Amenity as Amenity Entity (BusinessLogicLayer)
participant BaseModel as BaseModel (BusinessLogicLayer)
participant DB as Database (PersistenceLayer)

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