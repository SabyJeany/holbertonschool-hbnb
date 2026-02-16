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
