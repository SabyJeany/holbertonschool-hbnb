```mermaid

sequenceDiagram
autonumber
actor Client
participant API as API_REST
participant Auth as Authentication
participant Facade as Facade_Services
participant U as User
participant DB as DatabaseAccess

Client->>API: POST /register (email, password, names)
API->>Auth: verify_email_format(email)
Auth-->>API: OK

API->>Facade: register_user(data)
Facade->>U: new User(data)
Facade->>U: verify_email()
Facade->>U: save()
U->>DB: INSERT user
DB-->>U: user_id

Facade-->>API: user created
API-->>Client: 201 Created
