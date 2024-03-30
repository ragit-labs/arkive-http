from sqlalchemy import select
from arkive_db.models import User, Post
from typing import Sequence, Optional
from sqlalchemy import select
from fastapi import HTTPException
from arkive_web_service.database import db
from sqlalchemy.orm import selectinload
import uuid


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


async def get_all_cards_for_user(user_id: str) -> Sequence[Post]:
    query = select(User).options(selectinload(User.posts)).where(User.id == user_id)
    async with db.session() as session:
        result = (await session.execute(query)).scalars().one()
        return result.posts


async def get_post(post_id: str) -> Optional[Post]:
    async with db.session() as session:
        result = (
            await session.execute(select(Post).where(Post.id == post_id))
        ).scalar_one_or_none()
        return result


async def remove_post_for_user(post_id: str, user_id: str):
    async with db.session() as session:
        post = (
            await session.execute(select(Post).where(Post.id == post_id))
        ).scalar_one_or_none()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        user = (
            await session.execute(select(User).where(User.id == user_id))
        ).scalar_one_or_none()
        post.users.remove(user)
        await session.commit()
