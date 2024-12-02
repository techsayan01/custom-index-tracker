# Exports data to Excel and PDF
import pandas as pd
from fpdf import FPDF


class DataExporter:
    """
    Abstract class for exporting data.
    """
    def export(self, data: pd.DataFrame, filename: str):
        """
        Abstract method for exporting data. Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the `export` method.")


class ExcelExporter(DataExporter):
    """
    Exports data to an Excel file.
    """
    def export(self, data: pd.DataFrame, filename: str):
        """
        Exports data to an Excel file.

        Args:
            data: DataFrame containing the data to export.
            filename: The name of the output Excel file.
        """
        try:
            data.to_excel(filename, index=False, sheet_name="Index Performance")
            print(f"Data exported to Excel file: {filename}")
        except Exception as e:
            print(f"Failed to export data to Excel: {e}")


class PDFExporter(DataExporter):
    """
    Exports data to a PDF file.
    """
    def export(self, data: pd.DataFrame, filename: str):
        """
        Exports data to a PDF file.

        Args:
            data: DataFrame containing the data to export.
            filename: The name of the output PDF file.
        """
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Add a title
            pdf.cell(200, 10, txt="Index Performance Report", ln=True, align="C")
            pdf.ln(10)

            # Add data row by row
            for index, row in data.iterrows():
                pdf.cell(200, 10, txt=f"{row['date']}: {row['index_value']:.2f}", ln=True, align="L")

            pdf.output(filename)
            print(f"Data exported to PDF file: {filename}")
        except Exception as e:
            print(f"Failed to export data to PDF: {e}")


class DataExportManager:
    """
    Manages the export of data using different export formats.
    """
    def __init__(self):
        """
        Initializes the manager with available exporters.
        """
        self.exporters = {
            "excel": ExcelExporter(),
            "pdf": PDFExporter(),
        }

    def export(self, format: str, data: pd.DataFrame, filename: str):
        """
        Exports data using the specified format.

        Args:
            format: The format to use for exporting ("excel" or "pdf").
            data: DataFrame containing the data to export.
            filename: The name of the output file.
        """
        exporter = self.exporters.get(format.lower())
        if not exporter:
            raise ValueError(f"Unsupported export format: {format}")
        exporter.export(data, filename)
