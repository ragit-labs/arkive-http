import asyncio

from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import array_agg
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from arkive_db.models import Post, Tag
from arkive_web_service.post_filter_engine import (
    get_sqlalchemy_filter_clause,
    get_sqlalchemy_sort_clause,
)
from arkive_web_service.post_filter_engine.types import (
    GetAllRequestSort,
    GetAllRequestSortDirection,
    GetAllRequestWhere,
    GetAllRequestWhereField,
    GetAllRequestWhereFieldType,
    GetAllRequestWhereOperator,
)

DB_URI = "postgresql+asyncpg://arkive_admin:arkive1234@arkive-dev-do-user-16211520-0.c.db.ondigitalocean.com:25060/arkive_dev"

engine = create_async_engine(DB_URI, echo=True)

session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def main():
    where = GetAllRequestWhere(
        field=GetAllRequestWhereField(
            name="timestamp", type=GetAllRequestWhereFieldType.datetime
        ),
        value="2022-01-01T00:00:00",
        operator=GetAllRequestWhereOperator.gt,
    )
    filters = get_sqlalchemy_filter_clause([where])
    limit = 10
    skip = 4
    sort = GetAllRequestSort(
        field="timestamp", direction=GetAllRequestSortDirection.asc
    )
    sort_clause = get_sqlalchemy_sort_clause(sort)
    async with session_maker() as session:
        user_id = "78df8199-30a6-43fe-9373-ceef4e115328"
        keyword = "essay"
        query = select(Post).filter(
            Post.user_id == user_id,
            Post.title.ilike(f"%{keyword}%"),
        )
        result = (await session.execute(query)).scalars().all()
        for r in result:
            print(r.title)


asyncio.run(main())
