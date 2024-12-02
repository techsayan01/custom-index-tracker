import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from database_manager import DatabaseManager
import pandas as pd

class DataExporter:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def export_to_excel(self, filename: str):
        query = "SELECT * FROM index_performance"
        rows = self.db_manager.fetch_query(query)
        data = pd.DataFrame(rows, columns=['Date', 'IndexValue'])
        data.to_excel(filename, index=False)

    def export_to_pdf(self, filename: str):
        pdf = PdfPages(filename)

        query = "SELECT * FROM index_performance"
        rows = self.db_manager.fetch_query(query)
        data = pd.DataFrame(rows, columns=['Date', 'IndexValue'])

        plt.figure(figsize=(10, 6))
        plt.plot(data['Date'], data['IndexValue'], marker='o', linestyle='-', color='b')
        plt.title("Index Performance")
        plt.xlabel("Date")
        plt.ylabel("Index Value")
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        pdf.savefig()
        pdf.close()
