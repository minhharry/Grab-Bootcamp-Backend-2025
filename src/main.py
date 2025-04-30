from routers import dummy, restaurant, image_search
from fastapi import FastAPI
from contextlib import asynccontextmanager
from model_loader import load_model, cleanup_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield
    cleanup_model()

app = FastAPI(lifespan=lifespan)

app.include_router(dummy.router, prefix="/dummy")
app.include_router(image_search.router, prefix="/image_search")
app.include_router(restaurant.router, prefix="/restaurant")



