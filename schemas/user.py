from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The password for the user account.
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Schema for the token response after successful authentication.

    Attributes:
        access_token (str): The access token granted to the user.
        token_type (str): The type of the token (e.g., 'bearer').
    """
    access_token: str
    token_type: str
