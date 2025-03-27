from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    A Pydantic settings class to manage configuration variables.

    This class loads configuration values from environment variables or an `.env` file.
    It provides easy access to critical settings like the database URL, JWT secret key,
    and the JWT algorithm used in the application.

    Attributes:
        database_url (str): The URL of the database to connect to.
        jwt_secret_key (str): The secret key used to sign JWT tokens.
        jwt_algorithm (str): The algorithm used to sign JWT tokens. Defaults to "HS256".

    Configuration is loaded from the `.env` file, if it exists.

    Example:
        settings = Settings()
        print(settings.database_url)
    """

    # The URL for the database
    database_url: str

    # The secret key for signing JWT tokens
    jwt_secret_key: str

    # The algorithm for signing JWT tokens. Default is "HS256"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Initialize the settings object by loading values from environment variables or `.env`
settings = Settings()
