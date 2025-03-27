from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.post import create_post, get_posts_by_user, delete_post_by_id
from database.session import get_db
from dependencies.auth import get_current_user
from schemas.post import PostCreate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/add")
async def add_post(post: PostCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Create a new post for the authenticated user.

    Args:
        post (PostCreate): The post data to be created.
        user: The currently authenticated user.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the post content exceeds the allowed size.

    Returns:
        dict: The ID of the created post.
    """
    if len(post.content.encode('utf-8')) > 1024 * 1024:
        raise HTTPException(status_code=400, detail="Maximum post size is 1MB")
    new_post = await create_post(db, post, user.id)
    return {"postID": new_post.id}


@router.get("/get")
async def get_posts(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Retrieve all posts created by the authenticated user.

    Args:
        user: The currently authenticated user.
        db (AsyncSession): The database session.

    Returns:
        dict: A list of the user's posts with their IDs and content.
    """
    posts = await get_posts_by_user(db, user.id)
    return {"posts": [{"id": post.id, "content": post.content} for post in posts]}


@router.delete("/delete/{post_id:int}")
async def delete_post(post_id: int, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Delete a specific post by its ID, if it belongs to the authenticated user.

    Args:
        post_id (int): The ID of the post to delete.
        user: The currently authenticated user.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the post is not found or the user does not have permission to delete it.

    Returns:
        dict: A success message upon successful deletion.
    """
    deleted_post = await delete_post_by_id(db, post_id, user.id)
    if not deleted_post:
        raise HTTPException(status_code=404, detail="Post not found or you don't have permission to delete it")
    return {"message": "Post deleted successfully"}
