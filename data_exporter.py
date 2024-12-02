import pandas as pd

class Exporter:
    """Exports data to Excel and PDF formats."""
    def to_excel(self, data: pd.DataFrame, filename: str):
        data.to_excel(filename, index=False)

    def to_pdf(self, data: pd.DataFrame, filename: str):
        from matplotlib.backends.backend_pdf import PdfPages
        with PdfPages(filename) as pdf:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.axis('tight')
            ax.axis('off')
            ax.table(cellText=data.values, colLabels=data.columns, loc='center')
            pdf.savefig(fig)
