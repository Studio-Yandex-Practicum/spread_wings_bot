from django.conf import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


async def start_session():
    """Async connect with db."""
    engine = create_async_engine(settings.DB_URL)
    session = async_sessionmaker(engine, class_=AsyncSession)
    return session()
