```mermaid


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
    BusinessLogicLayer --> PersistenceLayer : CRUD Operations