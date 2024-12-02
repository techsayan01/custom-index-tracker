import matplotlib.pyplot as plt
from database_manager import DatabaseManager
from data_exporter import DataExporter
import pandas as pd

class Dashboard:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.exporters = DataExporter(db_manager)

    def plot_index_performance(self):
        #TODO query can be moved to a custom class
        query = "SELECT * FROM index_performance"
        rows = self.db_manager.fetch_query(query)
        data = pd.DataFrame(rows, columns=['Date', 'IndexValue'])

        # Convert 'Date' to a pandas datetime for better formatting
        data['Date'] = pd.to_datetime(data['Date'])

        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['IndexValue'], marker='o', linestyle='-', color='b')
        plt.title("Index Performance Over the Past Month", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Index Value", fontsize=12)

        # Format the x-axis
        plt.xticks(data['Date'][::2], rotation=45)  # Show every other date for better readability
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Automatically adjust layout to avoid overlap
        plt.tight_layout()
        plt.show()


    def plot_composition_changes(self):
        #TODO query can be moved to a custom class
        query = """
        SELECT Date, COUNT(DISTINCT Ticker) as CompositionChanges
        FROM stock_prices
        GROUP BY Date
        """
        rows = self.db_manager.fetch_query(query)
        data = pd.DataFrame(rows, columns=['Date', 'CompositionChanges'])

        # Convert 'Date' to pandas datetime
        data['Date'] = pd.to_datetime(data['Date'])

        plt.figure(figsize=(12, 6))
        bars = plt.bar(data['Date'], data['CompositionChanges'], color='orange', width=0.6)

        # Highlight values with annotations
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Only label meaningful values
                plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{int(height)}',
                         ha='center', va='bottom', fontsize=9)

        plt.title("Composition Changes Over the Past Month", fontsize=14)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Number of Changes in Composition", fontsize=12)
        
        # Format x-axis
        plt.xticks(data['Date'], rotation=45)

        # Dynamically set y-axis range
        plt.ylim(0, max(data['CompositionChanges']) + 1)

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def launch_dashboard(self):
        """Main function to launch the dashboard."""
        print("1. Plot Index Performance")
        print("2. Plot Index Composition for a Date")
        print("3. Export the data-set to pdf")
        print("4. Export the dataset to xlsx")
        print("5. Exit")

        while True:
            choice = input("Select an option (1-5): ")
            if choice == "1":
                self.plot_index_performance()
            elif choice == "2":
                self.plot_composition_changes()
            elif choice == "3":
                self.exporters.export_to_excel("index_data.xlsx")
            elif choice == "4":
                self.exporters.export_to_pdf("index_data.pdf")
            elif choice == "5":
                print("Exiting Dashboard.")
                break
            else:
                print("Invalid choice. Please select a valid option.")
