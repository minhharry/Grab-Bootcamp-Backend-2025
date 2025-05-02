CREATE TABLE restaurants (
    restaurant_id UUID PRIMARY KEY,
    restaurant_name TEXT,
    avatar_url TEXT,
    restaurant_description TEXT,
    opening_hours TEXT,
    price_range JSON,
    address TEXT,
    source TEXT NOT NULL,
    restaurant_rating FLOAT,
    restaurant_rating_count INTEGER,
    restaurant_url TEXT,
    crawl_time TIMESTAMP,
    crawl_id TEXT
);

CREATE TABLE reviews (
    review_id UUID PRIMARY KEY,
    restaurant_id UUID REFERENCES restaurants(restaurant_id),
    user_rating FLOAT,
    user_review TEXT,
    review_user_name TEXT,
    review_date TEXT
);

CREATE TABLE images (
    img_id UUID PRIMARY KEY,
    restaurant_id UUID REFERENCES restaurants(restaurant_id),
    food_name TEXT,
    food_price TEXT,
    img_url TEXT
);

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
);

CREATE TYPE FOOD_PREFERENCE  AS ENUM ('VEGAN', 'OMNIVORE');
CREATE TYPE GENDER AS ENUM ('MALE', 'FEMALE');
CREATE TYPE PRICE_RANGE_LEVEL AS ENUM ('1', '2', '3');

CREATE TABLE profiles (
    user_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    dietary_preference FOOD_PREFERENCE DEFAULT 'OMNIVORE',
    gender GENDER,
    date_of_birth DATE,
    preferred_price_range PRICE_RANGE_LEVEL,
    preferred_restaurant_types JSONB, -- [ "Vietnamese", "Italian", "Vegan" ]
    preferred_foods JSONB, -- [ "Pho", "Pizza" ]
);