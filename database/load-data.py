import json
from sqlalchemy import create_engine, text
import json
import glob
import os

# Đọc biến môi trường
POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')

DATABASE_URL = os.getenv('DATABASE_URL', f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

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
                    restaurant_id, restaurant_name, address, source,
                    restaurant_rating, restaurant_rating_count,
                    restaurant_url, crawl_time, crawl_id
                ) VALUES (
                    :restaurant_id, :restaurant_name, :address, :source,
                    :restaurant_rating, :restaurant_rating_count,
                    :restaurant_url, :crawl_time, :crawl_id
                )
                ON CONFLICT (restaurant_id) DO NOTHING
            """), {
                "restaurant_id": restaurant_id,
                "restaurant_name": entry.get("restaurant_name"),
                "address": entry.get("address"),
                "source": entry.get("source"),
                "restaurant_rating": entry.get("restaurant_rating"),
                "restaurant_rating_count": entry.get("restaurant_rating_count"),
                "restaurant_url": entry.get("restaurant_url"),
                "crawl_time": entry.get("crawl_time"),
                "crawl_id": entry.get("crawl_id")
            })
            
            for review in entry.get("reviews", []):
                conn.execute(text("""
                    INSERT INTO reviews (review_id, restaurant_id, user_rating, user_review)
                    VALUES (:review_id, :restaurant_id, :user_rating, :user_review)
                """), {
                    "review_id": review.get("review_id"),
                    "restaurant_id": restaurant_id,
                    "user_rating": review.get("user_rating"),
                    "user_review": review.get("user_review")
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
                    "img_url": img.get("img_url")
                })

if __name__ == "__main__":
    
    directory_path = "./input"
    
    if not os.path.isdir(directory_path):
        print(f"Thư mục không tồn tại: {directory_path}")
        
    else:
        jsonl_files = glob.glob(os.path.join(directory_path, "*.jsonl"))
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
