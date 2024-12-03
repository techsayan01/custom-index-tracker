from src.market_data_fetcher import MarketDataFetcher
from database.database_manager import DatabaseManager
from database.query_manager import QueryManager
from src.index_constructor import IndexConstructor
from src.data_exporter import DataExporter
from src.dashboard import Dashboard
import pandas as pd


def main():
    # Step 1: Configuration
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NFLX"]

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
    
    # formatted_data = [
    # ("2024-11-01", "AAPL", 174.55, 2900000000000),
    # ("2024-11-01", "MSFT", 330.12, 2430000000000),
    # ("2024-11-01", "GOOGL", 140.65, 1930000000000),
    # ("2024-11-02", "AAPL", 175.00, 2920000000000),
    # ("2024-11-02", "NFLX", 300.00, 1500000000000),
    # ("2024-11-02", "TSLA", 250.00, 1300000000000),
    # ("2024-11-03", "GOOGL", 142.00, 1950000000000),
    # ("2024-11-03", "AMZN", 117.00, 1600000000000),
    # ("2024-11-03", "NFLX", 310.00, 1550000000000)
    # ]

    # query_manager.insert_stock_data(formatted_data)



    # Step 4: Construct Index
    dates = prices.index.strftime("%Y-%m-%d").tolist()
    # dates = ["2024-11-05", "2024-11-06", "2024-11-07"]
    
    # Initialize index constructor
    index_constructor = IndexConstructor(query_manager)
    # Build the index data
    index_data = index_constructor.build_index(dates)
    composition_changes = query_manager.get_composition_changes(dates)
    # for change in composition_changes:
    #     print(change)

    # Step 5: Export Data
    exporter = DataExporter()
    exporter.export_to_excel(index_data, "index_performance.xlsx")
    exporter.export_to_pdf(index_data, "index_performance.pdf")

    # Step 6: Create Dashboard
    dashboard = Dashboard(index_data, composition_changes, query_manager)
    dashboard.run()


if __name__ == "__main__":
    main()
