```mermaid
erDiagram
    users {
        char(36) id PK
        varchar first_name
        varchar last_name
        varchar email
        varchar password
        boolean is_admin
    }

    places {
        char(36) id PK
        varchar title
        text description
        decimal price
        float latitude
        float longitude
        char(36) owner_id FK
    }

    reviews {
        char(36) id PK
        text text
        int rating
        char(36) user_id FK
        char(36) place_id FK
    }

    amenities {
        char(36) id PK
        varchar name
    }

    place_amenity {
        char(36) place_id FK
        char(36) amenity_id FK
    }

    users ||--o{ places : "owns"
    users ||--o{ reviews : "writes"
    places ||--o{ reviews : "receives"
    places }o--o{ amenities : "has"
    place_amenity }|--|| places : ""
    place_amenity }|--|| amenities : ""