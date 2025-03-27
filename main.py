from fastapi import FastAPI

from database.session import init_db
from routers import post, auth

# Initialize the FastAPI application
app = FastAPI()

# Include the authentication and post routers into the app
app.include_router(auth.router)
app.include_router(post.router)


@app.on_event("startup")
async def startup():
    """
    The startup event handler for the FastAPI application.

    This function is called when the application starts up. It is responsible for
    initializing the database connection by calling the `init_db()` function.

    This ensures that the database connection is ready before the application starts handling requests.
    """
    await init_db()
