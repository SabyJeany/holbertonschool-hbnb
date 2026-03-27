-- schema.sql

-- Table User
CREATE TABLE IF NOT EXISTS User (
    id          CHAR(36) PRIMARY KEY,
    first_name  VARCHAR(255) NOT NULL,
    last_name   VARCHAR(255) NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    is_admin    BOOLEAN DEFAULT FALSE
);

-- Table Place
CREATE TABLE IF NOT EXISTS Place (
    id          CHAR(36) PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    price       DECIMAL(10, 2) NOT NULL,
    latitude    FLOAT NOT NULL,
    longitude   FLOAT NOT NULL,
    owner_id    CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id)
);

-- Table Review
CREATE TABLE IF NOT EXISTS Review (
    id          CHAR(36) PRIMARY KEY,
    text        TEXT NOT NULL,
    rating      INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    user_id     CHAR(36) NOT NULL,
    place_id    CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    UNIQUE (user_id, place_id)  -- One review per user per place
);

-- Table Amenity
CREATE TABLE IF NOT EXISTS Amenity (
    id   CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Table Place_Amenity (many-to-many)
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id    CHAR(36) NOT NULL,
    amenity_id  CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);