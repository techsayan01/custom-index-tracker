import sqlite3
from typing import Optional

class DatabaseManager:
    def __init__(self, db_name: str = "stocks.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS stock_prices (
                Date TEXT NOT NULL,
                Ticker TEXT NOT NULL,
                Close REAL NOT NULL,
                PRIMARY KEY (Date, Ticker)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS market_caps (
                Ticker TEXT NOT NULL PRIMARY KEY,
                MarketCap REAL NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS index_performance (
                Date TEXT NOT NULL PRIMARY KEY,
                IndexValue REAL NOT NULL
            )
            """
        ]
        cursor = self.connection.cursor()
        for query in queries:
            cursor.execute(query)
        self.connection.commit()

    def execute_query(self, query: str, params: Optional[tuple] = None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()

    def fetch_query(self, query: str, params: Optional[tuple] = None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    def close_connection(self):
        self.connection.close()
