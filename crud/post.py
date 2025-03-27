from aiocache import cached
from aiocache.serializers import PickleSerializer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.post import Post
from schemas.post import PostCreate


async def create_post(db: AsyncSession, post: PostCreate, user_id: int):
    """
    Create a new post in the database.

    Args:
        db (AsyncSession): The database session.
        post (PostCreate): The post data to be created.
        user_id (int): The ID of the user creating the post.

    Returns:
        Post: The newly created post.
    """
    db_post = Post(user_id=user_id, content=post.content)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


@cached(ttl=300, serializer=PickleSerializer())
async def get_posts_by_user(db: AsyncSession, user_id: int):
    """
    Retrieve all posts by a specific user with caching.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The ID of the user whose posts are being retrieved.

    Returns:
        List[Post]: A list of posts created by the user.
    """
    result = await db.execute(select(Post).where(Post.user_id == user_id))
    return result.scalars().all()


async def delete_post_by_id(db: AsyncSession, post_id: int, user_id: int):
    """
    Delete a post by its ID if it belongs to the specified user.

    Args:
        db (AsyncSession): The database session.
        post_id (int): The ID of the post to be deleted.
        user_id (int): The ID of the user who owns the post.

    Returns:
        Optional[Post]: The deleted post if found, otherwise None.
    """
    result = await db.execute(select(Post).where(Post.id == post_id, Post.user_id == user_id))
    post = result.scalars().first()
    if not post:
        return None
    await db.delete(post)
    await db.commit()
    return post
