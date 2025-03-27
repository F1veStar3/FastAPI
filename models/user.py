from sqlalchemy import Column, Integer, String

from database.session import Base


class User(Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
        id (int): The primary key of the user.
        email (str): The unique email address of the user.
        hashed_password (str): The hashed password of the user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
