from data_fetcher import YahooFinanceFetcher, DataFetcher
from data_exporter import Exporter
from index_calculator import IndexCalculator
from database_manager import DatabaseManager
from data_exporter import Exporter
from dashboard import Dashboard


if __name__ == "__main__":
    # Initialize components
    db_manager = DatabaseManager()
    data_fetcher = YahooFinanceFetcher()
    index_calculator = IndexCalculator(db_manager)
    exporter = Exporter()
    dashboard = Dashboard(db_manager, index_calculator)

    # Fetch data example
    symbols = ["AAPL", "MSFT", "GOOG"]  # Replace with the top stock symbols
    stock_data = data_fetcher.fetch_data(symbols, "2023-11-01", "2023-11-30")
    print(stock_data)

    if not stock_data.empty:
        db_manager.insert_data(stock_data)
        print("Stock data successfully fetched and stored in the database.")

        # Export to Excel
        exporter.to_excel(stock_data, "stock_data.xlsx")
        print("Stock data exported to stock_data.xlsx.")

        # Launch dashboard
        dashboard.launch_dashboard(start_date="2023-11-01", end_date="2023-11-30", selected_date="2023-11-15")
    else:
        print("Failed to fetch stock data. Please check the symbols and date range.")
