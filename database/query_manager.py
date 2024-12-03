from database.database_manager import DatabaseManager

class QueryManager:
    """
    Handles all database queries.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.conn = self.db_manager.get_connection()

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
        result = self.query(query, (selected_date,))
        return [row[0] for row in result]


    def query(self, sql, params=()):
        """
        Executes a custom query and returns the results.
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    def get_composition_changes(self, dates):
        """
        Calculates the composition changes between consecutive trading days.

        Args:
            dates: List of dates in chronological order.

        Returns:
            List of dictionaries with keys ['date', 'added', 'removed'].
        """
        composition_changes = []
        previous_top_100 = set()

        for date in dates:
            # Fetch the top 100 stocks for the current date
            current_top_100 = set(self.get_top_100_stocks(date))  # Returns a set of tickers

            # Identify stocks that were added or removed
            added = current_top_100 - previous_top_100
            removed = previous_top_100 - current_top_100

            # Append the changes for this date
            composition_changes.append({
                "date": date,
                "added": list(added),  # Convert sets to lists for JSON compatibility
                "removed": list(removed)
            })

            # Update the previous set
            previous_top_100 = current_top_100

        return composition_changes


    def get_stock_prices(self, selected_date, tickers):
        """
        Fetches the prices of the specified tickers on the given date.

        Args:
            selected_date: The selected date to fetch data for.
            tickers: List of stock tickers.

        Returns:
            Dictionary mapping tickers to their prices.
        """
        placeholders = ",".join(["?"] * len(tickers))  # Creates a string like ?,?,?
        query = f"""
            SELECT ticker, price
            FROM stock_data
            WHERE date = ? AND ticker IN ({placeholders})
        """
        params = (selected_date, *tickers)
        result = self.query(query, params)

        # Convert prices to float to ensure numeric operations
        return {row[0]: float(row[1]) for row in result if isinstance(row[1], (int, float, str)) and row[1] != ""}
