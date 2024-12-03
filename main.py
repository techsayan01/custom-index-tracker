from src.market_data_fetcher import MarketDataFetcher
from database.database_manager import DatabaseManager
from database.query_manager import QueryManager
from src.index_constructor import IndexConstructor
from src.data_exporter import DataExporter
from src.dashboard import Dashboard
import pandas as pd


def main():
    # Step 1: Configuration
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

    # Step 2: Initialize Managers
    db_manager = DatabaseManager()
    query_manager = QueryManager(db_manager)

    # Step 3: Fetch and Persist Data
    fetcher = MarketDataFetcher(tickers, period="1mo")
    prices, market_caps = fetcher.fetch_data()

    formatted_data = [
        (date, ticker, prices.at[date, ticker], market_caps.at[date, ticker])
        for date in prices.index for ticker in prices.columns
    ]
    query_manager.insert_stock_data(formatted_data)

    # Step 4: Construct Index
    dates = prices.index.strftime("%Y-%m-%d").tolist()
    constructor = IndexConstructor(query_manager)
    index_data, composition_changes = constructor.build_index(dates)

    # Step 5: Export Data
    exporter = DataExporter()
    exporter.export_to_excel(index_data, "index_performance.xlsx")
    exporter.export_to_pdf(index_data, "index_performance.pdf")

    # Step 6: Create Dashboard
    dashboard = Dashboard(index_data, composition_changes, query_manager)
    dashboard.run()


if __name__ == "__main__":
    main()
