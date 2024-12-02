# Manages database operations (in-memory SQLite)

import sqlite3
from typing import List, Tuple


class DatabaseConnection:
    """
    Manages the database connection and setup.
    """
    def __init__(self, db_path: str = ":memory:"):
        """
        Initializes the connection to an SQLite database.

        Args:
            db_path: Path to the SQLite database file. Default is in-memory.
        """
        self.db_path = db_path
        self.conn = self._connect()

    def _connect(self) -> sqlite3.Connection:
        """
        Establishes a connection to the database.

        Returns:
            sqlite3.Connection: The database connection object.
        """
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def get_connection(self) -> sqlite3.Connection:
        """
        Provides the active database connection.

        Returns:
            sqlite3.Connection: The database connection object.
        """
        return self.conn

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()


class DatabaseManager:
    """
    Handles database operations for stock data.
    """
    def __init__(self, connection: DatabaseConnection):
        """
        Initializes the database manager with a connection.

        Args:
            connection: An instance of DatabaseConnection.
        """
        self.conn = connection.get_connection()
        self._create_table()

    def _create_table(self):
        """
        Creates the stock_data table if it doesn't exist.
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

    def insert_data(self, data: List[Tuple[str, str, float, float]]):
        """
        Inserts stock data into the database.

        Args:
            data: List of tuples with (date, ticker, price, market_cap).
        """
        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT OR REPLACE INTO stock_data (date, ticker, price, market_cap)
            VALUES (?, ?, ?, ?)
        """, data)
        self.conn.commit()

    def query_top_100(self, date: str) -> List[Tuple[str, float, float]]:
        """
        Retrieves the top 100 stocks by market cap for a specific date.

        Args:
            date: The date to filter the stock data.

        Returns:
            List of tuples with (ticker, price, market_cap).
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT ticker, price, market_cap
            FROM stock_data
            WHERE date = ?
            ORDER BY market_cap DESC
            LIMIT 100
        """, (date,))
        return cursor.fetchall()

    def close_connection(self):
        """
        Closes the database connection via the connection manager.
        """
        self.conn.close()


if __name__ == "__main__":
    # Step 1: Setup database connection and manager
    db_connection = DatabaseConnection()
    db_manager = DatabaseManager(db_connection)

    # Step 2: Insert example data
    example_data = [
        ("2024-11-01", "AAPL", 174.55, 2900000000000),
        ("2024-11-01", "MSFT", 328.77, 2430000000000),
        ("2024-11-01", "GOOGL", 140.65, 1930000000000),
        ("2024-11-02", "AAPL", 176.85, 2920000000000),
        ("2024-11-02", "MSFT", 330.25, 2445000000000),
    ]
    db_manager.insert_data(example_data)

    # Step 3: Query top 100 stocks for a specific date
    top_100 = db_manager.query_top_100("2024-11-01")
    print("Top 100 Stocks on 2024-11-01:")
    for stock in top_100:
        print(stock)

    # Step 4: Close the database connection
    db_manager.close_connection()

