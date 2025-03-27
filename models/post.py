from sqlalchemy import Column, Integer, Text

from database.session import Base


class Post(Base):
    """
    SQLAlchemy model representing a post.

    Attributes:
        id (int): The primary key of the post.
        user_id (int): The ID of the user who created the post.
        content (str): The text content of the post.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
