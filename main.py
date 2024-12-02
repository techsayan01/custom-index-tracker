from database_manager import DatabaseManager
from data_fetcher import StockDataFetcher
from index_calculator import IndexCalculator
from dashboard import Dashboard
from data_exporter import DataExporter
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 


if __name__ == "__main__":
    stock_db = os.getenv("STOCK_DB")
    db_manager = DatabaseManager(stock_db)
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Example tickers
    start_date = "2024-10-01"
    end_date = "2024-10-31"

    # Data fetching
    fetcher = StockDataFetcher(db_manager)
    fetcher.fetch_stock_data(tickers, start_date, end_date)
    fetcher.fetch_market_cap(tickers)

    # Index calculation
    constructor = IndexCalculator(db_manager)
    constructor.calculate_index()

    # Visualization
    dashboard = Dashboard(db_manager)
    dashboard.launch_dashboard()

    # # Export
    # exporter = DataExporter(db_manager)
    # exporter.export_to_excel("index_data.xlsx")
    # exporter.export_to_pdf("index_data.pdf")

    db_manager.close_connection()
