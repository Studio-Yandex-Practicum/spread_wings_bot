import pymysql

from src.bot.core.config import settings

try:
    connection = pymysql.connect(
        host=settings.host,
        user=settings.user,
        password=settings.password
    )
    print('connect')
    try:
        with connection.cursor() as cursor:
            info = "SHOW DATABASES"
            cursor.execute(info)
            res = cursor.fetchall()
            print(res)
    finally:
        connection.close()
except Exception as e:
    print(f'not connect because: {e}')
