from database.query_manager import QueryManager as query_manager
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

class Dashboard:
    """
    Creates and manages the dashboard visualization.
    """
    def __init__(self, index_data, composition_changes, query_manager):
        """
        Initialize the dashboard with data.

        Args:
            index_data: DataFrame containing index performance with columns ['date', 'index_value'].
            composition_changes: List of dictionaries with keys ['date', 'added', 'removed'].
            query_manager: Instance of QueryManager for database queries.
        """
        self.index_data = index_data
        self.composition_changes = composition_changes
        self.query_manager = query_manager  # Store QueryManager instance
        self.app = Dash(__name__)

    def create_layout(self):
        """
        Creates the layout of the dashboard.
        """
        self.app.layout = html.Div([
            html.H1("Index Dashboard", style={"textAlign": "center"}),

            # Line chart for index performance
            dcc.Graph(
                id="performance-chart",
                figure={
                    "data": [
                        go.Scatter(
                            x=self.index_data["date"],
                            y=self.index_data["index_value"],
                            mode="lines",
                            name="Index Performance"
                        )
                    ],
                    "layout": {"title": "Index Performance Over the Past Month"}
                }
            ),

            # Dropdown for selecting a date
            html.Div([
                html.H2("Select a Date for Composition"),
                dcc.Dropdown(
                    id="date-dropdown",
                    options=[{"label": date, "value": date} for date in self.index_data["date"]],
                    value=self.index_data["date"].iloc[0],
                    style={"width": "50%"}
                )
            ], style={"marginTop": "20px"}),

            # Bar chart for index composition
            dcc.Graph(id="composition-chart"),

            # Table for composition changes
            html.Div([
                html.H2("Composition Changes"),
                html.Table(
                    id="composition-table",
                    children=[
                        html.Tr([html.Th("Date"), html.Th("Added"), html.Th("Removed")])
                    ] + [
                        html.Tr([
                            html.Td(change["date"]),
                            html.Td(", ".join(change["added"])),
                            html.Td(", ".join(change["removed"]))
                        ]) for change in self.composition_changes
                    ],
                    style={"width": "100%", "border": "1px solid black", "marginTop": "20px"}
                )
            ])
        ])

    def register_callbacks(self):
        """
        Registers callbacks for interactivity.
        """
        @self.app.callback(
            Output("composition-chart", "figure"),
            Input("date-dropdown", "value")
        )
        def update_composition_chart(selected_date):
            """
            Updates the composition chart to show the distribution of stocks in the index on the selected date.
            Fetches data dynamically from the SQLite3 database.
            """
            # Query the database for top 100 stocks by market cap for the selected date
            result = self.query_manager.get_top_100_stocks(selected_date)

            # Prepare data for the chart
            tickers = [row[0] for row in result]  # Stock tickers
            market_caps = [row[1] for row in result]  # Market caps
            total_market_cap = sum(market_caps)  # Total market cap of top 100 stocks

            # Calculate weights (as percentages of total market cap)
            weights = [cap / total_market_cap for cap in market_caps]

            # Create a bar chart
            return {
                "data": [
                    go.Bar(
                        x=tickers,
                        y=weights,
                        text=[f"{weight * 100:.1f}%" for weight in weights],
                        textposition="auto",
                        name="Stock Weights"
                    )
                ],
                "layout": {
                    "title": f"Index Composition on {selected_date}",
                    "xaxis": {"title": "Stock Tickers"},
                    "yaxis": {"title": "Weight in Index"},
                    "barmode": "group",
                }
            }

    def run(self):
        """
        Runs the dashboard application.
        """
        self.create_layout()
        self.register_callbacks()
        self.app.run_server(debug=True)


# Main Workflow
if __name__ == "__main__":
    # Example index performance data
    index_data = pd.DataFrame({
        "date": ["2024-11-01", "2024-11-02", "2024-11-03"],
        "index_value": [100.0, 102.5, 101.8]
    })

    # Example composition changes
    composition_changes = [
        {"date": "2024-11-02", "added": ["TSLA"], "removed": ["GOOGL"]},
        {"date": "2024-11-03", "added": ["NFLX"], "removed": ["MSFT"]}
    ]

    # Create and run the dashboard
    dashboard = Dashboard(index_data, composition_changes, query_manager)
    dashboard.run()
