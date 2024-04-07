import uuid
from typing import Optional, Sequence

from fastapi import HTTPException
from sqlalchemy import select

from arkive_db.models import Post, Tag, User
from arkive_web_service.database import db

from ..post_filter_engine import (
    get_sqlalchemy_filter_clause,
    get_sqlalchemy_sort_clause,
)
from ..post_filter_engine.types import (
    GetAllRequest,
    GetAllRequestSort,
    GetAllRequestSortDirection,
)
from ..types import PostInsertRequestData


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


async def get_all_posts_for_user_conditioned(
    user_id: str, get_all_request: GetAllRequest
) -> Sequence[Post]:
    filters = (
        get_sqlalchemy_filter_clause(get_all_request.where)
        if get_all_request.where
        else None
    )
    limit = get_all_request.limit if get_all_request.limit else 10
    skip = get_all_request.skip if get_all_request.skip else 0
    sort_clause = (
        get_sqlalchemy_sort_clause(get_all_request.sort)
        if get_all_request.sort
        else get_sqlalchemy_sort_clause(
            GetAllRequestSort(
                field="timestamp", direction=GetAllRequestSortDirection.desc
            )
        )
    )
    async with db.session() as session:
        query = select(Post).filter(Post.user_id == user_id)
        if filters:
            query = query.filter(*filters)
        query = query.order_by(sort_clause)
        query = query.limit(limit).offset(skip)
        result = (await session.execute(query)).scalars().all()
        return result


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
            user_id=post_request_data.user_id,
        )
        post.tags.extend(tags_in_db)
        post.tags.extend(new_tags)
        session.add(post)
        await session.commit()


async def update_post_for_user(
    user_id: str, post_id: Optional[str], title: Optional[str], content: Optional[str]
):
    if not title and not content:
        raise HTTPException(status_code=400, detail="No data to update")
    async with db.session() as session:
        post = (
            await session.execute(select(Post).where(Post.id == post_id))
        ).scalar_one_or_none()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        if str(post.user_id) != user_id:
            raise HTTPException(
                status_code=403, detail=f"You are not allowed to update this post {post.user_id} {user_id}"
            )
        if title:
            post.title = title
        if content:
            post.content = content
        await session.commit()
