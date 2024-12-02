# Creates an interactive dashboard using Dash
from dash import Dash, dcc, html
import plotly.graph_objs as go
import pandas as pd


class DashboardDataProvider:
    """
    Provides data required for the dashboard.
    """
    def __init__(self, index_data: pd.DataFrame, composition_changes: dict):
        """
        Initializes the data provider with index performance and composition changes.

        Args:
            index_data: A DataFrame containing index performance data with columns ['date', 'index_value'].
            composition_changes: A dictionary of composition changes, where keys are dates and values are lists of changes.
        """
        self.index_data = index_data
        self.composition_changes = composition_changes

    def get_index_performance(self) -> pd.DataFrame:
        """
        Returns the index performance data.
        """
        return self.index_data

    def get_composition_changes(self) -> dict:
        """
        Returns the composition changes data.
        """
        return self.composition_changes


class Dashboard:
    """
    Creates and manages an interactive dashboard.
    """
    def __init__(self, data_provider: DashboardDataProvider):
        """
        Initializes the Dashboard with a data provider.

        Args:
            data_provider: An instance of DashboardDataProvider to fetch data for the dashboard.
        """
        self.data_provider = data_provider
        self.app = Dash(__name__)

    def _create_layout(self):
        """
        Creates the layout of the dashboard.
        """
        index_data = self.data_provider.get_index_performance()

        # Line chart for index performance
        index_performance_chart = go.Scatter(
            x=index_data['date'],
            y=index_data['index_value'],
            mode='lines',
            name='Index Performance'
        )

        # Composition changes as a list
        composition_changes = self.data_provider.get_composition_changes()

        self.app.layout = html.Div([
            html.H1("Custom Index Dashboard", style={"textAlign": "center"}),

            dcc.Graph(
                id="index-performance-chart",
                figure={
                    "data": [index_performance_chart],
                    "layout": {"title": "Index Performance Over Time"}
                }
            ),

            html.Div([
                html.H2("Composition Changes"),
                html.Ul([
                    html.Li(f"{date}: {', '.join(f'{change['action']} {change['ticker']}' for change in changes)}")
                    for date, changes in composition_changes.items()
                ])
            ], style={"marginTop": "20px"})
        ])

    def run(self):
        """
        Runs the dashboard application.
        """
        self._create_layout()
        self.app.run_server(debug=True)
