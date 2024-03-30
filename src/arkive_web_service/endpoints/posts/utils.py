from sqlalchemy import select
from arkive_db.models import User, Post
from typing import Sequence, Optional
from sqlalchemy import select
from arkive_web_service.database import db
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime



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


async def create_post(user_id: str) -> uuid.UUID:
    async with db.session() as session:
        post = Post(
            description="Test Description",
            url="https://google.com",
            banner="https://www.devart.com/dbforge/postgresql/how-to-install-postgresql-on-macos/images/launch-installation.png",
            timestamp=datetime.now(),
            user_id=user_id,
        )
        session.add(post)
        await session.commit()
        return post.id


async def get_post(post_id: str) -> Optional[Post]:
    async with db.session() as session:
        result = (await session.execute(select(Post).where(Post.id == post_id))).scalar_one_or_none()
        return result
