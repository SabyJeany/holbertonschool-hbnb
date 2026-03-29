# HBnB - AirBnB Clone
# holbertonschool-hbnb
HBnB (AirBnB clone) is a step-by-step backend project that reproduces the core logic of a rental platform: object models, serialization, persistent storage, and CRUD operations through an interactive command-line interface. It serves as a foundation for future web, API, and database integration.


A RESTful API application built with Python and Flask, implementing a simplified AirBnB-like platform.

## Description

HBnB is a web application that allows users to manage places, reviews, and amenities. It follows a 3-tier architecture with a clear separation of concerns between the Presentation, Business Logic, and Persistence layers.

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py         # User endpoints
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       └── amenities.py     # Amenity endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py        # Base class (id, created_at, updated_at)
│   │   ├── user.py              # User entity
│   │   ├── place.py             # Place entity
│   │   ├── review.py            # Review entity
│   │   └── amenity.py           # Amenity entity
│   ├── services/
│   │   ├── __init__.py          # Facade
│   │   └── facade.py            # HBnBFacade (Facade pattern)
│   └── persistence/
│       ├── __init__.py
│       └── repository.py        # In-memory repository
├── config.py                    # App configuration
├── run.py                       # Entry point
├── requirements.txt
└── README.md
```

## Architecture

The application is built around 3 layers:

- **Presentation Layer** — Flask + flask-restx API endpoints (`app/api/`)
- **Business Logic Layer** — Core models and logic (`app/models/`)
- **Persistence Layer** — In-memory storage, replaced by SQLAlchemy in Part 3 (`app/persistence/`)

Communication between layers goes through the **Facade pattern** (`app/services/facade.py`), which acts as a single entry point for all business logic operations.

## Entities

- **User** — Manages user accounts with email validation and password hashing
- **Place** — Represents a rental place with location, price, owner, amenities and reviews
- **Review** — A user review for a place with a rating between 1 and 5
- **Amenity** — A feature associated with a place (e.g. Wi-Fi, Pool)

## Installation

### Prerequisites

- Python 3.8+
- pip

### Steps

```bash
""
 Clone the repository
 """
git clone <repository_url>
cd hbnb

""" Install dependencies
"""
pip install -r requirements.txt
```

 Requirements

```
flask
flask-restx
```

 Running the Application

```bash
python run.py
```

The application will start at `http://127.0.0.1:5000`.

The Swagger documentation is available at: `http://127.0.0.1:5000/api/v1/`

""" API Endpoints
"""

 Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Create a new user |
| GET | `/api/v1/users/` | Get all users |
| GET | `/api/v1/users/<id>` | Get a user by ID |
| PUT | `/api/v1/users/<id>` | Update a user |


 Amenities
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/amenities/` | Create a new amenity |
| GET | `/api/v1/amenities/` | Get all amenities |
| GET | `/api/v1/amenities/<id>` | Get an amenity by ID |
| PUT | `/api/v1/amenities/<id>` | Update an amenity |

### Places
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/places/` | Create a new place |
| GET | `/api/v1/places/` | Get all places |
| GET | `/api/v1/places/<id>` | Get a place by ID (with owner & amenities details) |
| PUT | `/api/v1/places/<id>` | Update a place |

### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/reviews/` | Create a new review |
| GET | `/api/v1/reviews/` | Get all reviews |
| GET | `/api/v1/reviews/<id>` | Get a review by ID |
| PUT | `/api/v1/reviews/<id>` | Update a review |
| DELETE | `/api/v1/reviews/<id>` | Delete a review |
| GET | `/api/v1/reviews/places/<place_id>/reviews` | Get all reviews for a place |

## Usage Examples

### Create a User
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com", "password": "123456"}'
```

### Create an Amenity
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

### Create a Place
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": " Apartment",
    "description": "A nice place to stay",
    "price": 100,
    "latitude": 45.9000,
    "longitude": 2.3522,
    "owner_id": "<user_id>"
  }'
```

### Create a Review
```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great stay!",
    "rating": 5,
    "place_id": "<place_id>",
    "user_id": "<user_id>"
  }'
```

## Notes

- This is **Part 2** of the project. Authentication  and a real database (SQLAlchemy) will be added in Part 3.
- Data is stored **in-memory** and will be lost when the server restarts.
- Passwords are stored in plain text for now — bcrypt hashing will be added in Part 3.

## Authors
Bokouabela-saby Jeany
Holberton School — HBnB Project

