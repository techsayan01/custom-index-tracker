import yfinance as yf
import pandas as pd


class MarketDataFetcher:
    """
    Fetches stock price and market cap data.
    """
    def __init__(self, tickers, period="1mo", interval="1d"):
        self.tickers = tickers
        self.period = period
        self.interval = interval

    def fetch_data(self):
        """
        Fetches price and market cap data for the given tickers.
        """
        data = yf.download(self.tickers, period=self.period, interval=self.interval)
        prices = data["Adj Close"]

        market_caps = pd.DataFrame()
        for ticker in self.tickers:
            ticker_obj = yf.Ticker(ticker)
            shares_outstanding = ticker_obj.info.get("sharesOutstanding", None)
            if shares_outstanding:
                market_caps[ticker] = prices[ticker] * shares_outstanding

        return prices, market_caps
