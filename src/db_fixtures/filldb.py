from mysql.connector import Error as MySQLError
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from queries import (
    CREATE_DB,
    INSERT_COORDINATORS_QUERY,
    INSERT_LEGAL_QUESTIONS_QUERY,
    INSERT_PSYCHOLOGY_QUESTIONS_QUERY,
    INSERT_SOCIAL_QUESTIONS_QUERY,
    SET_SQL_MODE,
    TABLES,
    USE_DB,
)


class DB_Connection:
    """Create db connection with context manager."""

    def __init__(
        self,
        user: str = "root",
        password: str = "password",
        host: str = "127.0.0.1",
    ) -> None:
        """Init db args for connect to db."""
        self.user = user
        self.password = password
        self.host = host

    def __enter__(self) -> MySQLConnection:
        try:
            self.conn = MySQLConnection(
                user=self.user,
                password=self.password,
                host=self.host,
            )
            return self.conn
        except MySQLError as err:
            if err.errno == errorcode.CR_CONN_HOST_ERROR:
                print('Подключите контейнер БД командой "make rundb"')
                exit(1)
            else:
                print(err.msg)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.close()


def create_database(cursor: MySQLCursor):
    """Create db with special name."""
    try:
        cursor.execute(CREATE_DB)
    except MySQLError as err:
        print("Ошибка при создании базы данных: {}".format(err))


def create_database_tables(cursor: MySQLCursor) -> None:
    """Create special tables in db."""
    cursor.execute(USE_DB)
    cursor.execute(SET_SQL_MODE)
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Создание таблицы {}: ".format(table_name), end="")
            cursor.execute(table_description)
        except MySQLError as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Такая таблица уже существует")
            else:
                print(err.msg)
        else:
            print("OK")


def insert_into_db(cursor: MySQLCursor) -> None:
    """Insert data in table."""
    try:
        print("Наполнение таблицы тестовыми данными: ", end="")
        cursor.execute(USE_DB)
        cursor.execute(INSERT_COORDINATORS_QUERY)
        cursor.execute(INSERT_SOCIAL_QUESTIONS_QUERY)
        cursor.execute(INSERT_PSYCHOLOGY_QUESTIONS_QUERY)
        cursor.execute(INSERT_LEGAL_QUESTIONS_QUERY)
    except MySQLError as err:
        print(err)
    else:
        print("OK")


def main():
    """Start fill db."""
    with DB_Connection() as conn:
        cursor = conn.cursor()
        create_database(cursor=cursor)
        create_database_tables(cursor=cursor)
        insert_into_db(cursor=cursor)
        cursor.close()
        conn.commit()


if __name__ == "__main__":
    main()
