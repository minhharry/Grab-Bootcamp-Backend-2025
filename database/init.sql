CREATE TABLE restaurants (
    restaurant_id UUID PRIMARY KEY,
    restaurant_name TEXT,
    avatar_url TEXT,
    restaurant_description TEXT,
    opening_hours TEXT,
    price_range TEXT,
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

CREATE TYPE food_preference AS ENUM ('VEGAN', 'OMNIVORE');

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profile (
    user_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    location VARCHAR(100),
    preference food_preference DEFAULT 'OMNIVORE',
    search_keywords TEXT[] DEFAULT '{}',
    clicked_dishes UUID[] DEFAULT '{}',
    clicked_restaurants UUID[] DEFAULT '{}',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);