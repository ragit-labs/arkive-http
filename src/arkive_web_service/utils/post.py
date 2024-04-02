from sqlalchemy import select
from arkive_db.models import User, Post, Tag
from typing import Sequence, Optional
from fastapi import HTTPException
from arkive_web_service.database import db
from sqlalchemy.orm import selectinload
import uuid
from ..types import PostInsertRequestData


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


async def insert_post_for_user(post_request_data: PostInsertRequestData):
    async with db.session() as session:
        user_query = select(User).where(User.id == post_request_data.user_id)
        user = (await session.execute(user_query)).scalar_one_or_none()

        tags_query = select(Tag).where(Tag.name.in_(post_request_data.tags))
        tags_in_db = (await session.execute(tags_query)).scalars().all()
        tag_names_in_db = [tag.name for tag in tags_in_db]
        new_tags = []

        for tag in post_request_data.tags:
            if tag not in tag_names_in_db:
                new_tag = Tag(id=uuid.uuid4(), name=tag)
                session.add(new_tag)
                new_tags.append(new_tag)

        await session.flush()

        post = Post(
            id=uuid.uuid4(),
            title=post_request_data.title,
            content=post_request_data.content,
            url=post_request_data.url,
            banner=post_request_data.banner,
            timestamp=post_request_data.timestamp,
            extra_metadata=post_request_data.extra_metadata,
        )
        post.users.append(user)
        post.tags.extend(tags_in_db)
        post.tags.extend(new_tags)
        session.add(post)
        await session.commit()
