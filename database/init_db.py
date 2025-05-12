from sqlalchemy.ext.asyncio import create_async_engine
from database.models import Base
from dotenv import load_dotenv

import os


load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL'))

async def init_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)