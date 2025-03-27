from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import get_user_by_email, create_user
from schemas.user import UserCreate, TokenResponse
from database.session import get_db
from services.auth import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user and return an access token.

    Args:
        user (UserCreate): The user data for registration.
        db (AsyncSession): The database session dependency.

    Raises:
        HTTPException: If the user already exists.

    Returns:
        dict: Access token and token type.
    """
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = await create_user(db, user)
    token = create_access_token(data={"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return an access token.

    Args:
        user (UserCreate): The login credentials.
        db (AsyncSession): The database session dependency.

    Raises:
        HTTPException: If the email or password is incorrect.

    Returns:
        dict: Access token and token type.
    """
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
