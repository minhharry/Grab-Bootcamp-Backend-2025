from fastapi import HTTPException
from .model import DummyItem

# Fake database
dummy_db = {}

async def create_dummy(item: DummyItem):
    item_id = len(dummy_db) + 1
    dummy_db[item_id] = item
    return {"id": item_id, "item": item}

async def get_dummy(item_id: int):
    if item_id not in dummy_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "item": dummy_db[item_id]}
