from routers import dummy, image_search
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from sqlalchemy import text

app = FastAPI()

app.include_router(dummy.router, prefix="/dummy")
app.include_router(image_search.router, prefix="/image_search")


