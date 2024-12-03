import sqlite3
from settings.config import Config
import datetime
import pandas as pd

# Register adapters for pandas.Timestamp
sqlite3.register_adapter(pd.Timestamp, lambda ts: ts.strftime("%Y-%m-%d"))



class SingletonMeta(type):
    """
    Singleton metaclass to ensure a single instance of the DatabaseManager.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseManager(metaclass=SingletonMeta):
    """
    Manages the SQLite database with a singleton connection.
    """
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_PATH)
        self._create_tables()

    def _create_tables(self):
        """
        Creates the necessary database tables.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                date TEXT,
                ticker TEXT,
                price REAL,
                market_cap REAL,
                PRIMARY KEY (date, ticker)
            )
        """)
        self.conn.commit()

    def get_connection(self):
        """
        Returns the database connection.
        """
        return self.conn

    def query(self, query, params=()):
        """
        Executes a query and returns the results.
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
