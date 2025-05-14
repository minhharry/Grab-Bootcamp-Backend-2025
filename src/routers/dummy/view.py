from fastapi import APIRouter
from .model import DummyItem
from .controller import create_dummy, get_dummy

router = APIRouter()

@router.post("/", tags = ["Dummy"])
async def create(item: DummyItem):
    return await create_dummy(item)

@router.get("/{item_id}", tags = ["Dummy"])
async def get(item_id: int):
    return await get_dummy(item_id)
