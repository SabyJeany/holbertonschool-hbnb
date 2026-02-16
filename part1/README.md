 Airbnb Clone (Architecture + Models + API Flows)

Ce dépôt présente la conception (architecture + modèles + scénarios API) d’une application de type AIRBNB : gestion d’utilisateurs, de lieux (places), d’avis (reviews) et d’équipements (amenities), exposée via une ""API REST"", avec une logique métier claire et une couche de persistance.


 Objectifs

- Mettre en place une architecture plusieurs en "couches" (Presentation / Business / Persistence)
- Centraliser l’accès métier via un ""Facade Pattern""
- Définir les ""modèles"" (User, Place, Review, Amenity) héritant d’un parent `BaseModel`
- Décrire les principaux méthode (register, create place, create review, search places)


 Architecture globale

- ""Presentation Layer "": API REST, façade de services, authentification
- "Business Logic Layer" : modèles et règles métier
- "Persistence Layer" : stockage (DB / fichiers) .


classDiagram
    class PresentationLayer {
        <<Interface>>
        +API_REST
        +Facade_Services
        +Authentication
    }
    
    class BusinessLogicLayer {
        <<Models>>
        +User
        +Place
        +Review
        +Amenity
        +BaseModel
    }
    
    class PersistenceLayer {
        <<Repository>>
        +DatabaseAccess
        +FileStorage
    }
    
    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Storage Operations

    
 Modèles & relations

Les entités métiers héritent d’un BaseModel (id UUID4, timestamps, méthodes CRUD de base) et se relient entre elles :

Un User possède plusieurs Place : Relation one-to-many

Un User peut écrire plusieurs Review : Relation one-to-many

Un Place peut avoir plusieurs Amenity : Relation one-to-many

Un Place reçoit plusieurs Review : Relation many-to-many

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
        - verify_email()
        + get_average_rating()

        
    }
    
    class Place {
        - owner_id: UUID4
        + name : string 
        + description : string
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
    
    class Review {
    + place_id : UUID4
    + user_id : UUID4
    + rating : integrer
    + comments : string
    + list_by_place()
    + list_by_user()
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

     Workflows API (séquences)
     
1) Inscription utilisateur — POST /register

Validation des inputs

Vérification email unique

Hash du mot de passe

Génération UUID + timestamps

Sauvegarde DB + réponse JSON a l'aide de la méthode to_dict sequenceDiagram
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
 else Email is unique
     DB-->>User: Email not found 
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

 Schéma
┌─────────────┐
│ JEANY       │  "Je veux m'inscrire avec saby@example.com"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SERVEUR   │  "Attends, je vérifie si cet email existe déjà..."
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  BASE DE    │  "Je cherche saby@example.com..."
│  DONNÉES    │  "Trouvé ! Marie utilise déjà cet email !"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SERVEUR   │  "Désolé Jeany, cet email est déjà pris !"
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    JEANY    │  Reçoit : ❌ "Erreur 400 : Email déjà utilisé"
└─────────────┘


 2) Création d’un lieu — POST /places

Extraction user depuis token

Création du Place et rattachement à owner_id

Validation prix / coordonnées

Ajout amenities

Save + réponse JSON

    ##sequenceDiagram##
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


3) Ajouter un avis — POST /places/{place_id}/reviews

Auth token

Vérifier existence du place

Empêcher double review

Insert review + recalcul moyenne


sequenceDiagram
autonumber
    participant Client as review(client) 
    participant API as API/Facade
    participant User as User
    participant Place as Place
    participant Review as Review
    participant DB as Database

    Client->>API: POST /places/{place_id}/reviews (token, rating, comments)

    API->>User: verify_password(token)
    alt Token invalide
        User-->>API: ERROR
        API-->>Client: 401 Unauthorized
    else Token valide
        User-->>API: OK (user_id)

        API->>Place: check_exists(place_id)
        Place->>DB: SELECT place

        alt Place not found
            DB-->>Place: not found
            Place-->>API: not found
            API-->>Client: 404 Not Found
        else Place found
            DB-->>Place: found

            API->>Review: check_already_reviewed(user_id, place_id)
            Review->>DB: SELECT review WHERE user_id & place_id

            alt Review already exists
                DB-->>Review: found
                Review-->>API: already reviewed
                API-->>Client: 400 Bad Request (Already reviewed)
            else No review yet
                DB-->>Review: none
                API->>Review: create(user_id, place_id, rating, comments)
                Review->>DB: INSERT review
                DB-->>Review: OK (review_id)

                API->>Place: update_average_rating(place_id)
                Place->>DB: compute average rating
                DB-->>Place: new average

                API-->>Client: 201 Created (review_data + new_average)
            end
        end
    end



4) Recherche de lieux — GET /places?max_price=...&amenities=...

Filtres pour la Place

ajouter des détails : rating moyen, amenities, reviews

Le confort : pour voir les équipements et services (Wi-Fi, piscine, etc.). 


sequenceDiagram
autonumber
    participant Client as User 
    participant API as API/Facade
    participant Place as Place Entity
    participant Review as Review Entity
    participant Amenity as Amenity Entity
    participant BaseModel as BaseModel
    participant DB as Database

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



    .
├── api/                # routes
├── services/           # facade 
├── models/             # BaseModel, User, Place, Review, Amenity
├── persistence/        # database access / file storage
├── tests/              # 
└── README.md


