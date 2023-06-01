import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.bot.core.config import settings

loop = asyncio.get_event_loop()

engine = create_async_engine(settings.db_url)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def exp_session():
    """For example."""
    try:
        async with async_session() as session:
            sql = await session.execute(text("SHOW TABLES"))
            result = sql.scalars().all()
            return f"conect ok: {result}"
    except Exception as e:
        print(f"ops: {e}")


print(loop.run_until_complete(exp_session()))
