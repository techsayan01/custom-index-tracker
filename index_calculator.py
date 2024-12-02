# from database_manager import DatabaseManager

# class IndexCalculator:
#     """Calculates and tracks the custom equal-weighted index."""
#     def __init__(self, db_manager: DatabaseManager):
#         self.db_manager = db_manager
    
#     def calculate_index(self, date: str):
#         query = """
#         SELECT symbol, market_cap 
#         FROM stock_data 
#         WHERE date = ? 
#         ORDER BY market_cap DESC 
#         LIMIT 100
#         """
#         data = self.db_manager.query(query, (date,))
#         if not data:
#             return None
        
#         total_market_cap = sum([row[1] for row in data])
#         equal_weight = 1 / len(data) if data else 0

#         index_value = sum([equal_weight * row[1] / total_market_cap for row in data])
#         return index_value


# class IndexCalculator:
#     """Calculates and tracks the custom equal-weighted index."""
#     def __init__(self, db_manager: DatabaseManager):
#         self.db_manager = db_manager
    
#     def calculate_index(self, date: str):
#         query = """
#         SELECT symbol, market_cap 
#         FROM stock_data 
#         WHERE date = ? 
#         ORDER BY market_cap DESC 
#         LIMIT 100
#         """
#         data = self.db_manager.query(query, (date,))

#         if not data:
#             print(f"No data available for {date}.")
#             return None

#         # Filter out rows with None market_cap values
#         data = [row for row in data if row[1] is not None]

#         if not data:
#             print(f"No valid market cap data available for {date}.")
#             return None

#         total_market_cap = sum(row[1] for row in data)
#         equal_weight = 1 / len(data) if data else 0

#         # Calculate the index value
#         index_value = sum(equal_weight * row[1] / total_market_cap for row in data)
#         return index_value



import pandas as pd
from database_manager import DatabaseManager

class IndexCalculator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def calculate_index(self):
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
