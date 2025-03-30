from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str