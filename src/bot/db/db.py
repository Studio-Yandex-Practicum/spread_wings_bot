from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.core.config import settings


async def start_session():
    """Async connect with db."""
    engine = create_async_engine(settings.db_url)
    session = async_sessionmaker(engine, class_=AsyncSession)
    return session()
