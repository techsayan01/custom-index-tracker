import yfinance as yf
import pandas as pd
from abc import ABC, abstractmethod

class DataFetcher(ABC):
    """Abstract base class for fetching stock data."""
    @abstractmethod
    def fetch_data(self, symbols: list[str], start_date: str, end_date: str) -> pd.DataFrame:
        pass

class YahooFinanceFetcher(DataFetcher):
    """Concrete implementation using yfinance."""
    def fetch_data(self, symbols: list[str], start_date: str, end_date: str) -> pd.DataFrame:
        # Fetch data for all symbols using yfinance
        data = yf.download(symbols, start=start_date, end=end_date, group_by="ticker", auto_adjust=True)
        formatted_data = []

        # print(formatted_data)

        # Restructure data into a flat DataFrame
        for symbol in symbols:
            if symbol in data.columns.levels[0]:  # Check if the symbol has data
                symbol_data = data[symbol].reset_index()
                symbol_data["Symbol"] = symbol
                formatted_data.append(symbol_data)

        return pd.concat(formatted_data, ignore_index=True) if formatted_data else pd.DataFrame()
