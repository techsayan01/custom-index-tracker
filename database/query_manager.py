from database.database_manager import DatabaseManager

class QueryManager:
    """
    Handles all database queries.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.conn = db_manager.get_connection()

    def insert_stock_data(self, data):
        """
        Inserts stock data into the database.
        """
        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT OR REPLACE INTO stock_data (date, ticker, price, market_cap)
            VALUES (?, ?, ?, ?)
        """, data)
        self.conn.commit()

    # def get_top_100(self, date):
    #     """
    #     Retrieves the top 100 stocks by market cap for a given date.
    #     """
    #     cursor = self.conn.cursor()
    #     query = """
    #         SELECT ticker, price, market_cap
    #         FROM stock_data
    #         WHERE date = ?
    #         ORDER BY market_cap DESC
    #         LIMIT 100
    #     """
    #     cursor.execute(query, (date,))
    #     return cursor.fetchall()
    def get_top_100_stocks(self, selected_date):
        """
        Fetches the top 100 stocks by market cap for a specific date.

        Args:
            selected_date: The selected date to fetch data for.

        Returns:
            List of tuples with (ticker, market_cap).
        """
        query = """
            SELECT ticker, market_cap
            FROM stock_data
            WHERE date = ?
            ORDER BY market_cap DESC
            LIMIT 100
        """
        return self.query(query, (selected_date,))


    def query(self, sql, params=()):
        """
        Executes a custom query and returns the results.
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
