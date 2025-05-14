CREATE TABLE restaurants (
    restaurant_id UUID PRIMARY KEY,
    restaurant_name TEXT NOT NULL,
    avatar_url TEXT,
    restaurant_description TEXT,
    opening_hours TEXT,
    price_range JSON,
    address TEXT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    source TEXT NOT NULL,
    restaurant_rating FLOAT,
    restaurant_rating_count INTEGER,
    restaurant_url TEXT,
    crawl_time TIMESTAMP NOT NULL,
    crawl_id TEXT NOT NULL,
    restaurant_hash TEXT UNIQUE NOT NULL
);

CREATE TABLE reviews (
    review_id UUID PRIMARY KEY,
    restaurant_id UUID REFERENCES restaurants(restaurant_id) ON DELETE CASCADE NOT NULL,
    user_rating FLOAT,
    user_review TEXT,
    review_user_name TEXT,
    review_date TEXT,
    crawl_time TIMESTAMP NOT NULL,
    crawl_id TEXT NOT NULL,
    review_hash TEXT UNIQUE NOT NULL
);

CREATE TABLE images (
    img_id UUID PRIMARY KEY,
    restaurant_id UUID REFERENCES restaurants(restaurant_id) ON DELETE CASCADE NOT NULL,
    food_name TEXT NOT NULL,
    food_price TEXT,
    img_url TEXT NOT NULL,
    crawl_time TIMESTAMP NOT NULL,
    crawl_id TEXT NOT NULL,
    img_hash TEXT UNIQUE NOT NULL
);

CREATE INDEX idx_images_restaurant_id ON images(restaurant_id);

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TYPE FOOD_PREFERENCE  AS ENUM ('VEGAN', 'OMNIVORE');
CREATE TYPE GENDER AS ENUM ('MALE', 'FEMALE');
CREATE TYPE PRICE_RANGE_LEVEL AS ENUM ('1', '2', '3');

CREATE TABLE profiles (
    user_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    gender GENDER,
    date_of_birth DATE,
    preferred_price_range PRICE_RANGE_LEVEL,
    dietary_preference FOOD_PREFERENCE DEFAULT 'OMNIVORE'
);

CREATE TABLE user_restaurant_clicks (
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    restaurant_id UUID REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    click_count INTEGER DEFAULT 1,
    PRIMARY KEY (user_id, restaurant_id)
);

CREATE INDEX idx_reviews_restaurant_id ON reviews(restaurant_id); -- Tăng tốc tìm các đánh giá của một nhà hàng
CREATE INDEX idx_images_restaurant_id ON images(restaurant_id); -- Tăng tốc tìm các ảnh của một nhà hàng