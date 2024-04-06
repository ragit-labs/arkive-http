import asyncio
import uuid
from datetime import datetime

import requests
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from arkive_db.models import Post, User

lorem_picsum = "https://picsum.photos/200/300"


engine = create_async_engine(
    "postgresql+asyncpg://arkive_admin:arkive1234@localhost:5432/arkive"
)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def main():
    fake = Faker()

    async with async_session() as session:
        user_query = select(User).where(User.email == "akashm1219@gmail.com")
        user = (await session.execute(user_query)).scalar_one()
        image = requests.get(lorem_picsum)
        posts = [
            Post(
                id=uuid.uuid4(),
                title=fake.text(150),
                content=fake.text(7500),
                url=fake.url(),
                banner=str(image.url),
                extra_metadata={"author": fake.name()},
                timestamp=datetime.now(),
            )
            for i in range(30)
        ]
        session.add_all(posts)
        user.posts.extend(posts)
        await session.commit()


asyncio.run(main())
