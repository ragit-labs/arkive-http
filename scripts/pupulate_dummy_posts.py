from arkive_db.models import Post

import uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import asyncio
from datetime import datetime

engine = create_async_engine("postgresql+asyncpg://arkive_admin:arkive1234@localhost:5432/arkive")
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def main():
    async with async_session() as session:
        posts = [
            Post(
                id=uuid.uuid4(),
                description="ontrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a",
                url="https://www.lipsum.com/",
                banner="https://fastly.picsum.photos/id/474/200/200.jpg?hmac=X5gJb746aYb_1-VdQG2Cti4XcHC10gwaOfRGfs6fTNk",
                timestamp=datetime.now(),
                user_id="c3689fa0-ec19-4940-9286-5d75754c2cec",
            ) for x in range(20)
        ]
        session.add_all(posts)
        await session.commit()

asyncio.run(main())