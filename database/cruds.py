from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, func

from database.init_db import engine
from database.models import User


session_factory = async_sessionmaker(bind=engine)

async def add_user_if_not_exists(user_id: int) -> None:
    async with session_factory() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(user_id=user_id)
            session.add(user)
            await session.commit()

async def get_all_users() -> list[User] | None:
    async with session_factory() as session:
        users = await session.execute(select(User.user_id))
        return users.scalars().all()

async def get_amount_of_users() -> int:
    async with session_factory() as session:
        amount = await session.execute(select(func.count(User.user_id)))
        return amount.scalar()