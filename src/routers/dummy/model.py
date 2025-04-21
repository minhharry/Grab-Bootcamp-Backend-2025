from pydantic import BaseModel

# Schema
class DummyItem(BaseModel):
    name: str
    value: int
