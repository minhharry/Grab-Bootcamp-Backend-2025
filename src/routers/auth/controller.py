from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from .model import UserSignup, UserLogin, Token
from .service import signup_user, login_user
from fastapi import Form

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(data: UserSignup, db: Session = Depends(get_db)):
    signup_user(db, data)
    token = login_user(db, UserLogin(email=data.email, password=data.password))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_json(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, data)
    return {"access_token": token, "token_type": "bearer"}