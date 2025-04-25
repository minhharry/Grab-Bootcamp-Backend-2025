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
                    restaurant_id, restaurant_name, avatar_url, restaurant_description, address, source,
                    opening_hours, price_range, restaurant_rating, restaurant_rating_count,
                    restaurant_url, crawl_time, crawl_id
                ) VALUES (
                    :restaurant_id, :restaurant_name, :avatar_url, :restaurant_description, :address, :source,
                    :opening_hours, :price_range, :restaurant_rating, :restaurant_rating_count,
                    :restaurant_url, :crawl_time, :crawl_id
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
        
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO users (user_id, fullname, email, password_hash)
                VALUES
                    ('123e4567-e89b-12d3-a456-426614174001', 'Nguyen Phuc an chay', 'vegan@example.com', 'bcrypt_hash_001'),
                    ('123e4567-e89b-12d3-a456-426614174002', 'foodie_vn', 'foodie@example.com', 'bcrypt_hash_002'),
                    ('123e4567-e89b-12d3-a456-426614174003', 'Son Tung mtp', 'newbie@example.com', 'bcrypt_hash_003'),
                    ('123e4567-e89b-12d3-a456-426614174004', 'pizza_fan', 'pizza@example.com', 'bcrypt_hash_004'),
                    ('123e4567-e89b-12d3-a456-426614174005', 'indian_spice', 'indian@example.com', 'bcrypt_hash_005')
                ON CONFLICT (user_id) DO NOTHING
            """))
            print("Chèn dữ liệu users thành công!")
    except Exception as e:
        print(f"Lỗi khi chèn users: {e}")
        raise

    # Chèn profile
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO user_profiles (user_id, location, preference, gender, date_of_birth)
                VALUES
                    ('123e4567-e89b-12d3-a456-426614174001', '384 Nguyễn Trọng Tuyển, P. 2, Quận Tân Bình, TP. HCM', 'VEGAN', 'MALE', '1990-01-01'),
                    ('123e4567-e89b-12d3-a456-426614174002', '28 Phan Phú Tiên, P. 10, Quận 5, TP. HCM', 'OMNIVORE', 'FEMALE', '1995-05-05'),
                    ('123e4567-e89b-12d3-a456-426614174003', '577 Nguyễn Đình Chiểu, P. 2, Quận 3, TP. HCM', 'OMNIVORE', 'FEMALE', '1998-08-08'),
                    ('123e4567-e89b-12d3-a456-426614174004', '83 Hoàng Hoa Thám, P. 6, Quận Bình Thạnh, TP. HCM', 'OMNIVORE', 'MALE', '1992-02-02'),
                    ('123e4567-e89b-12d3-a456-426614174005', '113 Đào Duy Từ, Quận 10, TP. HCM', 'VEGAN', 'MALE', '1993-03-03')
                ON CONFLICT (user_id) DO NOTHING
            """))
            print("Chèn dữ liệu user_profiles thành công!")
    except Exception as e:
        print(f"Lỗi khi chèn user_profiles: {e}")
        raise
    
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO user_activies (user_id, search_keywords, clicked_dishes, clicked_restaurants)
                VALUES ('123e4567-e89b-12d3-a456-426614174001', 
                            ARRAY['chả giò chay', 'phở chay', 'salad'], 
                            ARRAY['123e4567-e89b-12d3-a456-426614171001', '123e4567-e89b-12d3-a456-426614171002']::UUID[], 
                            ARRAY['123e4567-e89b-12d3-a456-426614172001']::UUID[]),
                    ('123e4567-e89b-12d3-a456-426614174002', 
                            ARRAY['phở bò', 'bún chả', 'cơm tấm'], 
                            ARRAY['123e4567-e89b-12d3-a456-426614171003', '123e4567-e89b-12d3-a456-426614171004']::UUID[], 
                            ARRAY['123e4567-e89b-12d3-a456-426614172002', '123e4567-e89b-12d3-a456-426614172003']::UUID[]),
                    ('123e4567-e89b-12d3-a456-426614174003',
                            '{}', 
                            '{}', 
                            '{}'),
                    ('123e4567-e89b-12d3-a456-426614174004', 
                            ARRAY['pizza', 'pasta', 'tiramisu'], 
                            ARRAY['123e4567-e89b-12d3-a456-426614171005', '123e4567-e89b-12d3-a456-426614171006', '123e4567-e89b-12d3-a456-426614171007']::UUID[],
                            ARRAY['123e4567-e89b-12d3-a456-426614172004']::UUID[]),
                    ('123e4567-e89b-12d3-a456-426614174005', 
                            ARRAY['cà ri chay', 'naan', 'samosa'], 
                            ARRAY['123e4567-e89b-12d3-a456-426614171008']::UUID[], 
                            '{}')
                ON CONFLICT (user_id) DO NOTHING
            """))
            print("Chèn dữ liệu user_favorites thành công!")
    except Exception as e:
        print(f"Lỗi khi chèn profile: {e}")
        raise

if __name__ == "__main__":
    
    directory_path = "./input"
    
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
