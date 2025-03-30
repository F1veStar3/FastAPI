from aiocache import cached
from aiocache.serializers import PickleSerializer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.post import Post
from schemas.post import PostCreate


async def create_post(db: AsyncSession, post: PostCreate, user_id: int):
    db_post = Post(user_id=user_id, content=post.content)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


@cached(ttl=300, serializer=PickleSerializer())
async def get_posts_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Post).where(Post.user_id == user_id))
    return result.scalars().all()


async def delete_post_by_id(db: AsyncSession, post_id: int, user_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id, Post.user_id == user_id))
    post = result.scalars().first()
    if not post:
        return None
    await db.delete(post)
    await db.commit()
    return post
