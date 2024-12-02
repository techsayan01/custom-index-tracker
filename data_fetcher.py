# Handles fetching stock data from APIs

import yfinance as yf
import pandas as pd


import yfinance as yf
import pandas as pd


class DataSource:
    """
    Abstracts data fetching logic from a data source.
    """
    def __init__(self, tickers: list[str], period: str = "1mo", interval: str = "1d"):
        """
        Initializes the data source with the required parameters.

        Args:
            tickers: List of stock tickers to fetch data for.
            period: Time period for which data is required (e.g., '1mo', '6mo', '5y').
            interval: Interval of the data (e.g., '1d', '1wk').
        """
        self.tickers = tickers
        self.period = period
        self.interval = interval

    def fetch_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Fetches stock price and market cap data.

        Returns:
            Tuple of two DataFrames:
            - prices: Adjusted closing prices.
            - market_caps: Calculated market capitalizations.
        """
        try:
            # Fetch stock data
            data = yf.download(self.tickers, period=self.period, interval=self.interval)

            # Extract adjusted closing prices
            prices = data["Adj Close"]

            # Fetch shares outstanding using the Ticker object
            market_caps = pd.DataFrame()
            for ticker in self.tickers:
                ticker_obj = yf.Ticker(ticker)
                shares_outstanding = ticker_obj.info.get("sharesOutstanding", None)

                # Calculate market cap if shares outstanding is available
                if shares_outstanding:
                    market_caps[ticker] = prices[ticker] * shares_outstanding

            return prices, market_caps
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise


class DataFetcher:
    """
    Handles fetching and formatting of stock data.
    """
    def __init__(self, data_source: DataSource):
        """
        Initializes the data fetcher with a data source.

        Args:
            data_source: An instance of a DataSource object to fetch data.
        """
        self.data_source = data_source

    def get_formatted_data(self) -> list[tuple]:
        """
        Fetches and formats data for storage.

        Returns:
            A list of tuples in the format:
            (date, ticker, price, market_cap)
        """
        prices, market_caps = self.data_source.fetch_data()

        # Align and merge the prices and market caps
        formatted_data = []
        for date in prices.index:
            for ticker in prices.columns:
                # Ensure data exists for both price and market cap
                if ticker in market_caps.columns:
                    price = prices.at[date, ticker]
                    market_cap = market_caps.at[date, ticker]
                    formatted_data.append((date, ticker, price, market_cap))

        return formatted_data


if __name__ == "__main__":
    # Define stock tickers
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

    # Initialize the data source and fetcher
    data_source = DataSource(tickers=tickers, period="1mo", interval="1d")
    data_fetcher = DataFetcher(data_source)

    # Fetch and format the data
    formatted_data = data_fetcher.get_formatted_data()

    # Display the first few formatted rows
    print("Formatted Data:")
    for entry in formatted_data[:5]:
        print(entry)

