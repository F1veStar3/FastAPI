import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crud.user import get_user_by_email
from database.session import get_db

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                           db: AsyncSession = Depends(get_db)):
    """
    Retrieve the current authenticated user based on the JWT token.

    Args:
        credentials (HTTPAuthorizationCredentials): The authorization credentials containing the JWT token.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the token is invalid, expired, or the user is not found.

    Returns:
        User: The authenticated user object.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
