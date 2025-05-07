import sqlalchemy
from dotenv import load_dotenv
import os
from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import random
from model import Users, Restaurants, User_restaurant_clicks
from sqlalchemy.dialects.postgresql import insert

Base = declarative_base()

if __name__ == "__main__":
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL')

    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable không tìm thấy, kiểm tra lại .env")

    engine = sqlalchemy.create_engine(DATABASE_URL)

    Session = sessionmaker(bind=engine)
    session = Session()
    df = pd.read_csv("./users.csv")
    for i, row in df.iterrows():
        new_user = Users(user_id=row['user_id'], username=row['username'], email=row['email'], password_hash=row['password_hash'])
        session.add(new_user)
    session.commit()
    print("Đã thêm dummy user vào database!")

    restaurants = session.query(Restaurants).all()
    res_uuid_list = []
    for restaurant in restaurants:
        res_uuid_list.append(str(restaurant.restaurant_id))
    users = session.query(Users).all()
    user_uuid_list = []
    for user in users:
        user_uuid_list.append(str(user.user_id))
    res_uuid_list.sort()
    user_uuid_list.sort()
    random.seed(42) # For reproducibility
    for index, uid in enumerate(user_uuid_list):
        for i in range(random.randint(3, 10)):
            x = int(index/len(user_uuid_list)*len(res_uuid_list))
            if x + 20 > len(res_uuid_list):
                x = len(res_uuid_list) - 20
            res_uuid = random.choice(res_uuid_list[x:x+20])
            stmt = insert(User_restaurant_clicks).values(
                user_id=uid,
                restaurant_id=res_uuid,
                click_count=1
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id', 'restaurant_id'],
                set_={'click_count': User_restaurant_clicks.click_count + 1}
            )
            session.execute(stmt)
    session.commit()
    print("Đã thêm dummy user clicks data vào database!")

