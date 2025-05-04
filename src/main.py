from routers import dummy, restaurant, image_search, auth
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from model_loader import load_model, cleanup_model
from fastapi.middleware.cors import CORSMiddleware
from exception_handlers import http_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield
    cleanup_model()

app = FastAPI(lifespan=lifespan)

#Add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with actual origins allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(dummy.router, prefix="/dummy")
app.include_router(image_search.router, prefix="/image_search")
app.include_router(restaurant.router, prefix="/restaurant")
app.include_router(auth.router, prefix="/auth")


app.add_exception_handler(HTTPException, http_exception_handler)

