from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .model import UserSignup, UserLogin, UserProfile
from common_schemas.response import ApiResponse
from .service import signup_user, login_user, logout_user, get_current_user, get_profile_current_user
from database import get_db
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/auth/signup", response_model=ApiResponse, tags=["Authentication"])
def signup(data: UserSignup, db: Session = Depends(get_db)) -> ApiResponse:
    """
    Endpoint for user signup. Signs up a new user and logs them in to return a token.

    Args:
        data (UserSignup): The signup data containing email, password, etc.
        db (Session): The database session to interact with the DB.

    Returns:
        ApiResponse: Standardized response containing the access token.
    """
    result = signup_user(db, data)
    return result 


@router.post("/auth/login", response_model=ApiResponse, tags=["Authentication"])
def login(data: UserLogin, db: Session = Depends(get_db)) -> ApiResponse:
    """
    Endpoint for user login. Authenticates the user and returns a token.

    Args:
        data (UserLogin): The login data containing email and password.
        db (Session): The database session to interact with the DB.

    Returns:
        ApiResponse: Standardized response containing the access token.
    """
    result = login_user(db, data)
    return result

@router.post("/auth/logout", response_model=ApiResponse, tags=["Authentication"])
def logout(token: str = Depends(oauth2_scheme)) -> ApiResponse:
    """
    Endpoint for logging out a user.
    
    Args:
        token (str): The JWT token from the Authorization header.

    Returns:
        ApiResponse: A standardized response indicating successful logout.
    """
    return logout_user()

@router.get("/me", response_model=ApiResponse, tags=["Authentication"])
def get_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> ApiResponse:
    user_id = current_user.data.get("user_id")
    
    result = get_profile_current_user(db, user_id)  
    
    return result  # Return successful login ApiResponse.