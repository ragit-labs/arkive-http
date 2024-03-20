from arkive_db.models import User
from arkive_web_service.database import db
from sqlalchemy import select
from arkive_web_service.enums import SignInProvider
from typing import Optional


async def get_user_from_database(email: str):
    async with db.session() as session:
        query = select(User).where(User.email == email)
        user = (await session.execute(query)).scalars().one_or_none()
        return user


async def insert_user_to_database(
    email: str,
    full_name: str,
    first_name: str,
    siginin_provider: SignInProvider,
    last_name: Optional[str],
    display_picture_url: Optional[str],
):
    user = User(
        email=email,
        full_name=full_name,
        first_name=first_name,
        siginin_provider=siginin_provider,
        last_name=last_name,
        display_picture_url=display_picture_url,
    )

    async with db.session() as session:
        session.add(user)
        try:
            session.commit()
        except Exception as ex:
            raise Exception("Something went wrong while inserting the user", str(ex))
