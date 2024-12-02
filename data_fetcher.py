import yfinance as yf
from database_manager import DatabaseManager

class StockDataFetcher:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def fetch_stock_data(self, tickers, start_date, end_date):
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
        stock_data = data.reset_index().melt(id_vars='Date', var_name='Ticker', value_name='Close')
        for _, row in stock_data.iterrows():
            self.db_manager.execute_query(
                "INSERT OR REPLACE INTO stock_prices (Date, Ticker, Close) VALUES (?, ?, ?)",
                (row['Date'].strftime('%Y-%m-%d'), row['Ticker'], row['Close'])
            )

    def fetch_market_cap(self, tickers):
        market_caps = []
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            market_caps.append((ticker, stock.info.get('marketCap', 0)))
        for ticker, market_cap in market_caps:
            self.db_manager.execute_query(
                "INSERT OR REPLACE INTO market_caps (Ticker, MarketCap) VALUES (?, ?)",
                (ticker, market_cap)
            )
