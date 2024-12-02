import pandas as pd
from database_manager import DatabaseManager

class IndexCalculator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def calculate_index(self):
        # TODO - Query can be moved to custom file
        
        # Query top 100 stocks by market cap
        top_100_query = """
        SELECT sp.Date, sp.Ticker, sp.Close
        FROM stock_prices sp
        JOIN (SELECT Ticker FROM market_caps ORDER BY MarketCap DESC LIMIT 100) top_100
        ON sp.Ticker = top_100.Ticker
        """
        rows = self.db_manager.fetch_query(top_100_query)
        data = pd.DataFrame(rows, columns=['Date', 'Ticker', 'Close'])

        # Calculate equal-weighted index value
        data['WeightedPrice'] = data.groupby('Date')['Close'].transform(lambda x: x / len(x))
        index_performance = data.groupby('Date')['WeightedPrice'].sum().reset_index()
        for _, row in index_performance.iterrows():
            self.db_manager.execute_query(
                "INSERT OR REPLACE INTO index_performance (Date, IndexValue) VALUES (?, ?)",
                (row['Date'], row['WeightedPrice'])
            )
