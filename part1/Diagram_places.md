```mermaid
---
config:
  theme: dark
  look: neo
---
classDiagram
direction TB
    class PresentationLayer {
	    API/Services
	    User Interface
    }
    class BusinessLogicLayer {
	    ~~ User
	    ~~ Place
	    ~~ Review
	    ~~ Amenity
    }
    class PersistenceLayer {
	    ~~DatabaseAccess
	    ~~FilesStorage
    }
    PresentationLayer --o BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --o PersistenceLayer : Storage Operation
