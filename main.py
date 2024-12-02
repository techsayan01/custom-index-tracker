from data_fetcher import DataSource, DataFetcher
from database_manager import DatabaseManager
from index_analyzer import IndexAnalyzer
from index_builder import IndexBuilder
from data_exporter import DataExportManager
from dashboard import Dashboard, DashboardDataProvider


def main():
    # Step 1: Configuration
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    trading_dates = ["2024-11-01", "2024-11-02", "2024-11-03"]
    db_path = ":memory:"  # Use ":memory:" for in-memory database or specify a file path for persistent storage

    # Step 2: Initialize DatabaseManager with the database path
    print("Setting up database...")
    db_manager = DatabaseManager(db_path)

    # Step 3: Initialize Modules
    data_source = DataSource(tickers=tickers, period="1mo", interval="1d")
    data_fetcher = DataFetcher(data_source)
    analyzer = IndexAnalyzer(db_manager.get_connection())
    export_manager = DataExportManager()

    # Step 4: Fetch and Store Data
    print("Fetching and storing data...")
    formatted_data = data_fetcher.get_formatted_data()
    db_manager.insert_data(formatted_data)

    # Step 5: Build Index
    print("Building index...")
    builder = IndexBuilder(analyzer.get_top_100_stocks, trading_dates)
    index_df = builder.build_index()
    composition_changes = builder.track_composition_changes()

    # Step 6: Export Data
    print("Exporting data...")
    export_manager.export("excel", index_df, "index_performance.xlsx")
    export_manager.export("pdf", index_df, "index_performance.pdf")

    # Step 7: Create and Run Dashboard
    print("Starting dashboard...")
    dashboard_data_provider = DashboardDataProvider(index_df, composition_changes)
    dashboard = Dashboard(dashboard_data_provider)
    dashboard.run()


if __name__ == "__main__":
    main()
