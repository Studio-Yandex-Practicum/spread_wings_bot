import asyncio
import aiomysql

from src.bot.core.config import settings

loop = asyncio.new_event_loop()


async def python_mysql(inf: str):
    connection = await aiomysql.connect(
        host=settings.host,
        user=settings.user,
        password=settings.password,
    )

    cur = await connection.cursor()
    await cur.execute(inf)
    db = await cur.fetchall()
    print(db)
    await cur.close()
    connection.close()


loop.run_until_complete(python_mysql("SHOW DATABASES"))
