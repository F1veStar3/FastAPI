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
    await init_db()
