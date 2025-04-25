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

CREATE TYPE FOOD_PREFERENCE AS ENUM ('VEGAN', 'OMNIVORE');
CREATE TYPE GENDER AS ENUM ('MALE', 'FEMALE');

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fullname VARCHAR(50),
    email VARCHAR(100),
    password_hash VARCHAR(255)
);

CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    location VARCHAR(100),
    preference FOOD_PREFERENCE DEFAULT 'OMNIVORE',
    gender GENDER,
    date_of_birth DATE
);

CREATE TABLE user_activies (
    user_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    search_keywords TEXT[] DEFAULT '{}',
    clicked_dishes UUID[] DEFAULT '{}',
    clicked_restaurants UUID[] DEFAULT '{}'
)