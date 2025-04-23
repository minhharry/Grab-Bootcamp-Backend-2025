CREATE TABLE restaurants (
    restaurant_id UUID PRIMARY KEY,
    restaurant_name TEXT,
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
    user_review TEXT
);

CREATE TABLE images (
    img_id UUID PRIMARY KEY,
    restaurant_id UUID REFERENCES restaurants(restaurant_id),
    food_name TEXT,
    food_price TEXT,
    img_url TEXT
);
