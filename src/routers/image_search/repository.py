from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from typing import List, Dict

def get_image_restaurant_data(db: Session, img_ids: List[str]) -> Dict[str, dict]:
    query = text("""
        SELECT
            i.img_id, i.restaurant_id, i.food_name, i.food_price, i.img_url,
            r.restaurant_name, r.address, r.restaurant_rating, r.restaurant_url
        FROM images i
        LEFT JOIN restaurants r ON i.restaurant_id = r.restaurant_id
        WHERE i.img_id = ANY(ARRAY[:img_ids]::uuid[])
    """)
    rows = db.execute(query, {"img_ids": img_ids}).fetchall()
    return {str(row.img_id): dict(row._mapping) for row in rows}