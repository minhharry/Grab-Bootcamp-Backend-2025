from sqlalchemy.orm import Session
import pandas as pd
from uuid import UUID
from .model import User_restaurant_clicks
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import APIRouter
from common_schemas.response import ApiResponse
from database import get_db
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/", response_model=ApiResponse)
async def get(user_uuid: str, top_n: int = 20, session: Session = Depends(get_db)) -> ApiResponse:
    """
        Get recommendations for a user based on their click history similar to top_n other users, using cosine similarity.
        Args:
            user_uuid: The user's UUID in str.
            top_n: The number of users.
            session: The SQLAlchemy session object.
        Returns:
            A list of dict containing the recommendations.
    """
    user_uuid = UUID(user_uuid)
    records = session.query(
        User_restaurant_clicks.user_id,
        User_restaurant_clicks.restaurant_id,
        User_restaurant_clicks.click_count
    ).all()
    df = pd.DataFrame(records, columns=["user_id", "restaurant_id", "click_count"])
    if df.empty:
        return ApiResponse(
        status=200,
        message="Data retrieved successfully, but user_restaurant_clicks table in database is empty!",
        data=[],
        metadata=None 
    )
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
    except:
        raise HTTPException(
            status_code=500,
            detail="Failed to get recommendations!",
        )
    if not res:
        raise HTTPException(
            status_code=404,
            detail="No recommendations found"
        )
    return ApiResponse(
        status=200,
        message="Data retrieved successfully",
        data=res,  # List of dict of score, restaurant_id
        metadata=None 
    )
