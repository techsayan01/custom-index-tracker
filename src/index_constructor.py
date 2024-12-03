import pandas as pd

class IndexConstructor:
    """
    Constructs an equal-weighted custom index.
    """
    def __init__(self, query_manager):
        self.query_manager = query_manager


    def build_index(self, dates):
        """
        Constructs an equal-weighted index for the given dates.

        Args:
            dates: List of trading dates in chronological order.

        Returns:
            A pandas DataFrame containing the index value for each date with columns ['date', 'index_value'].
        """
        index_data = []

        for date in dates:
            # Fetch the top 100 stocks for the current date
            top_100_stocks = self.query_manager.get_top_100_stocks(date)

            # Fetch prices for the top 100 stocks
            stock_prices = self.query_manager.get_stock_prices(date, top_100_stocks)

            # Calculate the equal-weighted index value
            weight = 1 / len(top_100_stocks) if top_100_stocks else 0
            index_value = sum(price * weight for price in stock_prices.values())

            # Append the index value for the current date
            index_data.append({"date": date, "index_value": index_value})

        # print(top_100_stocks)
        # Convert to a pandas DataFrame
        return pd.DataFrame(index_data)