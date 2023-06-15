from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def extract_data_from_db(session: AsyncSession, sql_request: str) -> str:
    """Извлчение html таблицы контактов координаторов из БД."""
    data = await session.execute(text(sql_request))
    data = data.scalars().first()
    return data
