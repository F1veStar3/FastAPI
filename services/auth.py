import bcrypt
import jwt
from datetime import datetime, timedelta
from config import settings


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a JWT access token with the given data and an optional expiration time.

    Args:
        data (dict): A dictionary containing the data to encode in the JWT payload.
        expires_delta (timedelta, optional): The expiration time for the token. If not provided,
                                              the token will expire in 30 minutes by default.

    Returns:
        str: The encoded JWT token as a string.

    Example:
        token = create_access_token(data={"user_id": 123}, expires_delta=timedelta(hours=1))
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_password(plain_password, hashed_password):
    """
    Verifies if a plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.

    Example:
        is_valid = verify_password(plain_password="mysecretpassword", hashed_password="$2b$12$...")
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password):
    """
    Hashes a plain text password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password as a string.

    Example:
        hashed_password = get_password_hash(password="mysecretpassword")
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
