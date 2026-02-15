```mermaid

sequenceDiagram
autonumber

participant Client as review 
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
