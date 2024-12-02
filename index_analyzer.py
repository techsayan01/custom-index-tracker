# Analyzes database data (e.g., top 100 stocks)

from typing import List, Tuple
import sqlite3


class IndexAnalyzer:
    """
    Provides methods for analyzing stock data to identify key metrics
    like the top 100 stocks by market cap.
    """
    def __init__(self, connection: sqlite3.Connection):
        """
        Initializes the IndexAnalyzer with a database connection.

        Args:
            connection: An active SQLite database connection object.
        """
        self.conn = connection

    def get_top_100_stocks(self, date: str) -> List[Tuple[str, float, float]]:
        """
        Retrieves the top 100 stocks by market cap for a given date.

        Args:
            date: The date for which the analysis is to be performed.

        Returns:
            A list of tuples containing:
            - ticker: The stock ticker.
            - price: The stock's price on the given date.
            - market_cap: The stock's market capitalization on the given date.
        """
        cursor = self.conn.cursor()
        query = """
            SELECT ticker, price, market_cap
            FROM stock_data
            WHERE date = ?
            ORDER BY market_cap DESC
            LIMIT 100
        """
        cursor.execute(query, (date,))
        return cursor.fetchall()

    def calculate_daily_change(self, date: str) -> List[Tuple[str, float]]:
        """
        Calculates the percentage change in price for all stocks compared
        to the previous trading day.

        Args:
            date: The current date for which changes are calculated.

        Returns:
            A list of tuples containing:
            - ticker: The stock ticker.
            - daily_change: The percentage change in price.
        """
        cursor = self.conn.cursor()

        # Get current and previous day's data
        query = """
            WITH current_day AS (
                SELECT ticker, price
                FROM stock_data
                WHERE date = ?
            ),
            previous_day AS (
                SELECT ticker, price
                FROM stock_data
                WHERE date = (
                    SELECT MAX(date)
                    FROM stock_data
                    WHERE date < ?
                )
            )
            SELECT 
                c.ticker,
                ((c.price - p.price) / p.price) * 100 AS daily_change
            FROM current_day c
            JOIN previous_day p
            ON c.ticker = p.ticker
        """
        cursor.execute(query, (date, date))
        return cursor.fetchall()

    def get_composition_changes(self, current_date: str, previous_date: str) -> List[Tuple[str, str]]:
        """
        Compares the top 100 stock compositions between two dates to identify changes.

        Args:
            current_date: The current date for comparison.
            previous_date: The previous date for comparison.

        Returns:
            A list of tuples containing:
            - action: "Added" or "Removed".
            - ticker: The stock ticker that was added or removed.
        """
        cursor = self.conn.cursor()

        # Get top 100 stocks for both dates
        query_top_100 = """
            SELECT ticker
            FROM stock_data
            WHERE date = ?
            ORDER BY market_cap DESC
            LIMIT 100
        """

        cursor.execute(query_top_100, (current_date,))
        current_top_100 = {row[0] for row in cursor.fetchall()}

        cursor.execute(query_top_100, (previous_date,))
        previous_top_100 = {row[0] for row in cursor.fetchall()}

        # Determine added and removed stocks
        added = current_top_100 - previous_top_100
        removed = previous_top_100 - current_top_100

        changes = [("Added", ticker) for ticker in added] + [("Removed", ticker) for ticker in removed]
        return changes


if __name__ == "__main__":
    from database_manager import DatabaseConnection

    # Set up database connection and manager
    db_connection = DatabaseConnection()
    conn = db_connection.get_connection()
    print(conn)

    # Initialize the analyzer
    analyzer = IndexAnalyzer(conn)

    # Example usage
    date = "2024-11-01"
    previous_date = "2024-10-31"

    # Get top 100 stocks
    top_100 = analyzer.get_top_100_stocks(date)
    print("Top 100 Stocks by Market Cap:")
    for stock in top_100[:5]:  # Print only first 5 for brevity
        print(stock)

    # # Calculate daily changes
    # daily_changes = analyzer.calculate_daily_change(date)
    # print("\nDaily Percentage Changes:")
    # for change in daily_changes[:5]:  # Print only first 5 for brevity
    #     print(change)

    # # Get composition changes
    # composition_changes = analyzer.get_composition_changes(date, previous_date)
    # print("\nComposition Changes:")
    # for change in composition_changes:
    #     print(change)

    # # Close the connection
    # db_connection.close()

