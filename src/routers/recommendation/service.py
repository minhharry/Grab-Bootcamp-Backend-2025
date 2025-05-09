from sqlalchemy.orm import Session
from .repository import add_click, get_user_restaurant_clicks_by_restaurant, get_restaurants_by_ids, get_random_restaurants, get_user_clicks
from common_schemas.response import ApiResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sklearn.metrics.pairwise import cosine_similarity
from uuid import UUID
from typing import List
import pandas as pd

def add_click_to_restaurant(db: Session, user_id: str, restaurant_id: str) -> ApiResponse:
    """
    Business logic to handle adding a click for a user to a restaurant.

    Args:
        db: Database session
        user_id: User's UUID
        restaurant_id: Restaurant's UUID

    Returns:
        ApiResponse: The result, containing success or failure status and message.
    """
    if add_click(db, user_id, restaurant_id):
        return ApiResponse(
            status=200,
            message="Click added successfully",
            data=None,
            metadata=None
        )
    else:
        return HTTPException(
            status_code=500,
            detail="Failed to add click"
        )
    
def get_recommendations(user_uuid: UUID, top_n: int, session) -> List:
    """
    Get recommendations for a user based on their click history similar to top_n other users,
    using cosine similarity.

    Args:
        user_uuid (UUID): The user's UUID.
        top_n (int): The number of similar users to consider.
        session: The SQLAlchemy session object.

    Returns:
        list: A list of restaurant recommendations with scores.
    
    Raises:
        HTTPException: If there is an error during the recommendation calculation.
    """
    clicks = get_user_clicks(session)

    if clicks:
        records = [(click.user_id, click.restaurant_id, click.click_count) for click in clicks]
        
        df = pd.DataFrame(records, columns=["user_id", "restaurant_id", "click_count"])
    else:
        df = pd.DataFrame(columns=["user_id", "restaurant_id", "click_count"])

    if df.empty:
        return []
    try:
        matrix = df.pivot(index="user_id", columns="restaurant_id", values="click_count").fillna(0)
        arr = cosine_similarity(matrix, matrix)
        row_position = matrix.index.get_loc(user_uuid)
        user_row = matrix.iloc[row_position]
        user_non_zero_columns = user_row[user_row > 0.1].index.tolist()
        user_sim = arr[row_position].tolist()
        for i in range(len(user_sim)):
            user_sim[i] = (user_sim[i], i)
        user_sim.sort(key=lambda x: x[0], reverse=True)
        top_n = min(top_n, len(user_sim))
        top_n_sim = user_sim[:top_n]
        res = []
        passed = []
        for i in range(len(top_n_sim)):
            if top_n_sim[i][1] != row_position:
                sim_user_row = matrix.iloc[top_n_sim[i][1]]
                sim_user_non_zero_columns = sim_user_row[sim_user_row > 0.1].index.tolist()
                for x in sim_user_non_zero_columns:
                    if x not in user_non_zero_columns and x not in passed:
                        res.append({
                            "score": top_n_sim[i][0],
                            "restaurant_id": x,
                        })
                        passed.append(x)
        
        data_map = get_restaurants_by_ids(session, passed)
        detail_res = []
        for recommendation in res:
            restaurant_id = str(recommendation['restaurant_id'])
            restaurant_data = data_map.get(restaurant_id)
            if restaurant_data:
                detail_res.append({
                    "score": recommendation["score"],
                    "restaurant_id": restaurant_data.get("restaurant_id"),
                    "restaurant_name": restaurant_data.get("restaurant_name"),
                    "avatar_url": restaurant_data.get("avatar_url"),
                    "address": restaurant_data.get("address"),
                    "price_level": restaurant_data.get("price_level"),
                    "restaurant_rating": restaurant_data.get("restaurant_rating"),
                    "longitude": restaurant_data.get("longitude"),
                    "latitude": restaurant_data.get("latitude"),
                })
        if not res:
            raise HTTPException(
                status_code=404,
                detail="No recommendations found"
            )

        return detail_res

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations!")
    

def get_random_restaurants_details(db: Session, limit: int = 10) -> List:
    """
    Get details of random restaurants from the database.

    Args:
        db (Session): The database session.
        limit (int): The number of random restaurants to fetch (default is 10).

    Returns:
        list: A list of restaurant details with price levels.
    """
    restaurants = get_random_restaurants(db, limit)

    if not restaurants:
        return []

    return restaurants