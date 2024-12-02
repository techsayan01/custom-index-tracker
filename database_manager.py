import sqlite3
import pandas as pd

class DatabaseManager:
    """Manages SQLite database for storing stock data."""
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        # self.create_tables()
    
    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                symbol TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                market_cap REAL,
                PRIMARY KEY (symbol, date)
            )
            """)

    def insert_data(self, data: pd.DataFrame):
        print("inserting stock data from in sqlite3")
        with self.conn:
            data.to_sql("stock_data", self.conn, if_exists="append", index=False)

    def query(self, sql: str, params=None):
        print("query the sqlite3 database")
        with self.conn:
            cursor = self.conn.execute(sql, params or [])
            return cursor.fetchall()
