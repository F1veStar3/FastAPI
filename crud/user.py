from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user import User
from schemas.user import UserCreate
from services.auth import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str):
    """
    Retrieve a user by their email address.

    Args:
        db (AsyncSession): The database session.
        email (str): The email address of the user.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    """
    Create a new user in the database with a hashed password.

    Args:
        db (AsyncSession): The database session.
        user (UserCreate): The user data to be created.

    Returns:
        User: The newly created user.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
