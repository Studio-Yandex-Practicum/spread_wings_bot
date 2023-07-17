from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def extract_data_from_db(session: AsyncSession, sql_request: str) -> str:
    """Извлчение данных из БД с помощью sql-запроса."""
    data = await session.execute(text(sql_request))
    data = data.scalars().first()
    return data
