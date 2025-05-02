from .model import UserSignup, UserLogin, Token
from .repository import get_user_by_email, create_user_with_profile
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime
import re
from common_schemas.response import ApiResponse
from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return ApiResponse(
            status=401,
            message="Token expired"
        )
    except jwt.InvalidTokenError:
        return ApiResponse(
            status=401,
            message="Invalid token"
        )

def validate_email(email: str) -> bool:
    """
    Validate the email format.
    
    Args:
        email (str): The email to be validated.
    
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_gender(gender: str) -> bool:
    """
    Validate the gender to be either 'MALE' or 'FEMALE'.
    
    Args:
        gender (str): The gender to be validated.
    
    Returns:
        bool: True if the gender is valid, False otherwise.
    """
    return gender in ["MALE", "FEMALE"]

def validate_password(password: str) -> bool:
    """
    Validate the password to have at least 6 characters.
    
    Args:
        password (str): The password to be validated.
    
    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return len(password) >= 6

def validate_date_of_birth(dob: str) -> bool:
    """
    Validate the date_of_birth format to be in 'yyyy-mm-dd'.
    
    Args:
        dob (str): The date of birth to be validated.
    
    Returns:
        bool: True if the date_of_birth is valid, False otherwise.
    """
    try:
        datetime.strptime(dob, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def signup_user(db, user: UserSignup) -> ApiResponse:
    """
    Handles the user signup process, including checking for an existing email,
    hashing the password, and creating the user in the database.

    Args:
        db: Database session
        user: The user data received during signup

    Returns:
        ApiResponse: A response model containing the user data and token
    """
    # Validate email format
    if not validate_email(user.email):
        return ApiResponse(
            status=400,
            message="Invalid email format"
        )

    # Validate gender
    if not validate_gender(user.gender):
        return ApiResponse(
            status=400,
            message="Gender must be 'MALE' or 'FEMALE'"
        )

    # Validate password length
    if not validate_password(user.password):
        return ApiResponse(
            status=400,
            message="Password must be at least 6 characters long"
        )

    # Validate date of birth
    if not validate_date_of_birth(user.date_of_birth):
        return ApiResponse(
            status=400,
            message="Date of birth must be in the format 'yyyy-mm-dd'"
        )

    # Check if email is already registered
    if get_user_by_email(db, user.email):
        return ApiResponse(
            status=400,
            message="Email already registered"
        )

    # Hash the password
    hashed = hash_password(user.password)
    
    # Create the user and profile in the database
    created_user = create_user_with_profile(db, user, hashed)

    # Generate the access token
    token = create_access_token({"email": created_user.email, "sub": str(created_user.user_id)})

    # Return successful ApiResponse
    return ApiResponse(
        status=200,
        message="User signed up successfully",
        data={"access_token": token, "token_type": "bearer"},
        metadata=None
    )


def login_user(db, user: UserLogin) -> ApiResponse:
    """
    Handles the user login process, including checking credentials and generating
    a JWT token for the user.

    Args:
        db: Database session
        user: The user login data (email and password)

    Returns:
        ApiResponse: A response model containing the JWT token
    """
    # Validate email format
    if not validate_email(user.email):
        return ApiResponse(
            status=400,
            message="Invalid email format"
        )

    # Check if user exists in the database
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        return ApiResponse(
            status=401,
            message="Invalid credentials"
        )

    # Create and return the JWT token
    token = create_access_token({"email": db_user.email, "sub": str(db_user.user_id)})
    
    return ApiResponse(
        status=200,
        message="User logged in successfully",
        data={"access_token": token, "token_type": "bearer"},
        metadata=None
    )

def get_current_user(token: str = Depends(oauth2_scheme)) -> ApiResponse:
    """
    Retrieves the current logged-in user based on the JWT token.

    Args:
        token: The JWT token passed in the Authorization header.

    Returns:
        ApiResponse: A response model containing the user ID of the currently authenticated user.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return ApiResponse(
                status=401,
                message="Invalid token (no user_id)"
            )
        return ApiResponse(
            status=200,
            message="Current user retrieved successfully",
            data={"user_id": user_id},
            metadata=None
        )
    except ExpiredSignatureError:
        return ApiResponse(
            status=401,
            message="Token expired"
        )
    except InvalidTokenError:
        return ApiResponse(
            status=401,
            message="Invalid token"
        )

def logout_user() -> ApiResponse:
    """
    Handles the user logout process. 

    Returns:
        ApiResponse: A standardized response indicating successful logout.
    """
    return ApiResponse(
        status=200,
        message="User logged out successfully"
    )