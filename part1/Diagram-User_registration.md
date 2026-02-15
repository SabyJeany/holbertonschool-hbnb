```mermaid
sequenceDiagram
autonumber

 participant Client as User 
 participant API as API/Facade (PrésentationLayer)
 participant User as User Entity (BusinessLogicLayer)
 participant BaseModel as BaseModel (BusinessLogicLayer)
 participant DB as Database (PersistenceLayer)

Client->>API: POST /register (email, password, first_name, last_name)
API->>API: Validate input data

API->>User: verify_email(email) 
User->>DB: Check if email exists

alt Email already exists
    DB-->>User: Email found
    User-->>API: False 
    API-->>Client: 400 Bad Request (Email already registered) 
else Email is unique DB-->>User: Email not found 
    User-->>API: True 
    API->>User: create new User instance 
    User->>User: hash_password(password) 
    User->>BaseModel: Generate UUID (id) 
    User->>BaseModel: Set created_at 
    User->>BaseModel: Set updated_at 
    User->>BaseModel: save() 
    BaseModel->>DB: INSERT user 
    DB-->>BaseModel: Success 
    BaseModel->>BaseModel: to_dict() 
    BaseModel-->>API: User data (dict) 
    API-->>Client: 201 Created (user_data)
end