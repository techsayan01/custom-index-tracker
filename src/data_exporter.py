import os
import pandas as pd
from fpdf import FPDF


class DataExporter:
    """
    Exports data to Excel and PDF.
    """

    def __init__(self, output_folder="output"):
        """
        Initializes the DataExporter with an output folder.

        Args:
            output_folder: Folder where files will be saved.
        """
        self.output_folder = output_folder
        self._ensure_output_folder()

    def _ensure_output_folder(self):
        """
        Ensures the output folder exists.
        """
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def export_to_excel(self, data, filename="index_performance.xlsx"):
        """
        Exports data to an Excel file.

        Args:
            data: DataFrame containing the data to export.
            filename: Name of the Excel file.
        """
        filepath = os.path.join(self.output_folder, filename)
        data.to_excel(filepath, index=False)
        print(f"Exported to {filepath}")

    def export_to_pdf(self, data, filename="index_performance.pdf"):
        """
        Exports data to a PDF file.

        Args:
            data: DataFrame containing the data to export.
            filename: Name of the PDF file.
        """
        filepath = os.path.join(self.output_folder, filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for _, row in data.iterrows():
            pdf.cell(200, 10, txt=f"Date: {row['date']} | Index Value: {row['index_value']:.2f}", ln=True)
        pdf.output(filepath)
        print(f"Exported to {filepath}")
