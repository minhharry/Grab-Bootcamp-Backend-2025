import json
from sqlalchemy import create_engine, text
import json
import glob
import os
from dotenv import load_dotenv

# script_dir = os.path.dirname(os.path.abspath(__file__))
# load_dotenv(os.path.join(script_dir, "../.env"))
load_dotenv()
# Đọc biến môi trường
POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
POSTGRES_HOST = "localhost"  
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

def read_jsonl(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))
        return data
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        return []

def insert_data(jsonl_data):
    with engine.begin() as conn:  # dùng transaction tự động rollback nếu lỗi
        for entry in jsonl_data:
            restaurant_id = entry.get("restaurant_id")

            conn.execute(text("""
                INSERT INTO restaurants (
                    restaurant_id, 
                    restaurant_name, 
                    avatar_url, 
                    restaurant_description, 
                    address, 
                    longitude,
                    latitude,
                    source,
                    opening_hours, 
                    price_range, 
                    restaurant_rating, 
                    restaurant_rating_count,
                    restaurant_url, 
                    crawl_time, 
                    crawl_id
                ) VALUES (
                    :restaurant_id, 
                    :restaurant_name, 
                    :avatar_url, 
                    :restaurant_description, 
                    :address, 
                    :longitude,
                    :latitude,
                    :source,
                    :opening_hours, 
                    :price_range, 
                    :restaurant_rating, 
                    :restaurant_rating_count,
                    :restaurant_url, 
                    :crawl_time, 
                    :crawl_id
                )
                ON CONFLICT (restaurant_id) DO NOTHING
            """), {
                "restaurant_id": restaurant_id,
                "restaurant_name": entry.get("restaurant_name"),
                "avatar_url": entry.get("avatar_url"),
                "restaurant_description": entry.get("restaurant_description"),
                "opening_hours": entry.get("opening_hours"),
                "price_range": entry.get("price_range"),
                "address": entry.get("address"),
                "latitude": entry.get("latitude"),
                "longitude": entry.get("longitude"),
                "source": entry.get("source"),
                "restaurant_rating": entry.get("restaurant_rating"),
                "restaurant_rating_count": entry.get("restaurant_rating_count"),
                "restaurant_url": entry.get("restaurant_url"),
                "crawl_time": entry.get("crawl_time"),
                "crawl_id": entry.get("crawl_id")
            })
            
            for review in entry.get("reviews", []):
                conn.execute(text("""
                    INSERT INTO reviews (review_id, restaurant_id, user_rating, user_review, review_user_name, review_date)
                    VALUES (:review_id, :restaurant_id, :user_rating, :user_review, :review_user_name, :review_date)
                """), {
                    "review_id": review.get("review_id"),
                    "restaurant_id": restaurant_id,
                    "user_rating": review.get("user_rating"),
                    "user_review": review.get("user_review"),
                    "review_user_name": review.get("review_author"),
                    "review_date": review.get("review_date")
                })

            for img in entry.get("images", []):
                conn.execute(text("""
                    INSERT INTO images (img_id, restaurant_id, food_name, food_price, img_url)
                    VALUES (:img_id, :restaurant_id, :food_name, :food_price, :img_url)
                """), {
                    "img_id": img.get("img_id"),
                    "restaurant_id": restaurant_id,
                    "food_name": img.get("food_name"),
                    "food_price": img.get("food_price"),
                    "img_url": img.get("img_url"),
                })

if __name__ == "__main__":
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    directory_path = os.path.join(script_dir, "../processed_data")
    
    if not os.path.isdir(directory_path):
        print(f"Thư mục không tồn tại: {directory_path}")
        
    else:
        jsonl_files = glob.glob(os.path.join(directory_path, "*.json"))
        if not jsonl_files:
            print(f"Không tìm thấy file .jsonl trong thư mục: {directory_path}")
        else:
            for jsonl_file_path in jsonl_files:

                data = read_jsonl(jsonl_file_path)
                if data:
                    insert_data(data)
                    print("Dữ liệu đã được nạp thành công vào PostgreSQL.")
                else:
                    print("Không có dữ liệu để nạp.")
