import matplotlib.pyplot as plt
import pandas as pd
from database_manager import DatabaseManager
from index_calculator import IndexCalculator

class Dashboard:
    """Creates a dashboard using Matplotlib for visualizing index performance."""
    def __init__(self, db_manager: DatabaseManager, index_calculator: IndexCalculator):
        self.db_manager = db_manager
        self.index_calculator = index_calculator

    def plot_index_performance(self, start_date: str, end_date: str):
        """Plots the index performance over a given date range."""
        query = """
        SELECT DISTINCT date FROM stock_data 
        WHERE date BETWEEN ? AND ?
        ORDER BY date
        """
        dates = self.db_manager.query(query, (start_date, end_date))
        print("the date wise data is here")
        print(dates)
        dates = [row[0] for row in dates]

        index_values = [self.index_calculator.calculate_index(date) for date in dates]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, index_values, marker='o', linestyle='-', color='b', label='Index Value')
        plt.title('Index Performance')
        plt.xlabel('Date')
        plt.ylabel('Index Value')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.show()

    def plot_composition_changes(self, date: str):
        """Plots the composition of the index for a given date."""
        query = """
        SELECT symbol, market_cap 
        FROM stock_data 
        WHERE date = ?
        ORDER BY market_cap DESC 
        LIMIT 100
        """
        data = self.db_manager.query(query, (date,))
        print("printing stock_data")
        print(data)
        if not data:
            print("No data available for the selected date.")
            return

        symbols, market_caps = zip(*data)

        plt.figure(figsize=(12, 8))
        plt.bar(symbols[:20], market_caps[:20], color='orange')  # Show top 20 for readability
        plt.title(f'Top 20 Stocks by Market Cap on {date}')
        plt.xlabel('Stock Symbol')
        plt.ylabel('Market Cap (in billions)')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.grid(axis='y')
        plt.show()

    def show_summary_metrics(self, start_date: str, end_date: str):
        """Displays summary metrics such as cumulative return and composition changes."""
        query = """
        SELECT DISTINCT date FROM stock_data 
        WHERE date BETWEEN ? AND ?
        ORDER BY date
        """
        # query = """SELECT * FROM stock_data"""
        dates = self.db_manager.query(query, (start_date, end_date))
        dates = [row[0] for row in dates]

        index_values = [self.index_calculator.calculate_index(date) for date in dates]
        if not index_values:
            print("No data available for the selected period.")
            return

        # Calculate cumulative return and daily changes
        cumulative_return = (index_values[-1] - index_values[0]) / index_values[0] * 100
        daily_changes = [(index_values[i] - index_values[i - 1]) / index_values[i - 1] * 100 
                         for i in range(1, len(index_values))]

        print(f"Summary Metrics from {start_date} to {end_date}:")
        print(f"  Cumulative Return: {cumulative_return:.2f}%")
        print(f"  Average Daily Change: {pd.Series(daily_changes).mean():.2f}%")

    def launch_dashboard(self, start_date: str, end_date: str, selected_date: str):
        """Main function to launch the dashboard."""
        print("1. Plot Index Performance")
        print("2. Plot Index Composition for a Date")
        print("3. Show Summary Metrics")
        print("4. Exit")

        while True:
            choice = input("Select an option (1-4): ")
            if choice == "1":
                self.plot_index_performance(start_date, end_date)
            elif choice == "2":
                self.plot_composition_changes(selected_date)
            elif choice == "3":
                self.show_summary_metrics(start_date, end_date)
            elif choice == "4":
                print("Exiting Dashboard.")
                break
            else:
                print("Invalid choice. Please select a valid option.")
