from pydantic import BaseModel
from uuid import UUID


class Dish(BaseModel):
    img_id: UUID
    restaurant_id: UUID
    food_name: str
    food_price: str
    img_url: str