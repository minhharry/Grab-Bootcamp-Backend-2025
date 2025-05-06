from pydantic import BaseModel
from uuid import UUID

class UserRestaurantClick(BaseModel):
    user_id: UUID
    restaurant_id: UUID
    click_count: int = 1 
