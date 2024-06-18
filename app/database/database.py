import pymysql
# from app.config.config import Config
from pymysql.cursors import DictCursor


class Database:
    conn: pymysql.Connection = None
    curs: DictCursor = None

    @classmethod
    def init(cls):
        Database.conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            charset='utf8mb4',
            cursorclass=DictCursor)
        Database.curs = Database.conn.cursor()

    # @classmethod
    # def init(cls):
    #     Database.conn = pymysql.connect(
    #         host=Config.MYSQL_HOST,
    #         user=Config.MYSQL_USER,
    #         password=Config.MYSQL_PASSWORD,
    #         database=Config.MYSQL_DB,
    #         charset='utf8mb4',
    #         cursorclass=DictCursor)
    #     Database.curs = Database.conn.cursor()

    @classmethod
    def fetchall(cls, query: str, data: tuple = None) -> tuple:
        if data:
            Database.curs.execute(query, data)
        else:
            Database.curs.execute(query)
        print(f"Running Query: {query} Data: {data}")
        return Database.curs.fetchall()

    @classmethod
    def fetchone(cls, query: str, data: tuple) -> dict:
        Database.curs.execute(query, data)
        print(f"Running Query: {query} Data: {data}")
        return Database.curs.fetchone()

    @classmethod
    def executemany(cls, query: str, data: list[tuple]) -> None:
        print("Executing many...")
        Database.curs.executemany(query, data)
        Database.conn.commit()

    @classmethod
    def execute(cls, query: str, data: tuple) -> None:
        print("Executing one...")
        Database.curs.execute(query, data)
        Database.conn.commit()


if not Database.conn:
    Database.init()
