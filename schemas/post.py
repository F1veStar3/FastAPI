from pydantic import BaseModel


class PostCreate(BaseModel):
    """
    Schema for creating a new post.

    Attributes:
        content (str): The text content of the post.
    """
    content: str