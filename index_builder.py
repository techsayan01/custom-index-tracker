# Constructs the equal-weighted custom index
from typing import List, Dict
import pandas as pd


class IndexBuilder:
    """
    Constructs and manages an equal-weighted custom index.
    """
    def __init__(self, top_100_stocks_provider, dates: List[str]):
        """
        Initializes the IndexBuilder.

        Args:
            top_100_stocks_provider: A callable that provides top 100 stocks by market cap for a given date.
            dates: List of trading dates for which the index is built.
        """
        self.top_100_stocks_provider = top_100_stocks_provider
        self.dates = dates

    def build_index(self) -> pd.DataFrame:
        """
        Builds the equal-weighted index for the provided dates.

        Returns:
            A DataFrame with columns: ['date', 'index_value'].
        """
        index_data = []

        for date in self.dates:
            # Fetch top 100 stocks for the current date
            top_100_stocks = self.top_100_stocks_provider(date)

            # Calculate equal weight
            equal_weight = 1 / len(top_100_stocks)

            # Calculate the index value for the day
            index_value = sum(stock[1] * equal_weight for stock in top_100_stocks)
            index_data.append({"date": date, "index_value": index_value})

        return pd.DataFrame(index_data)

    def track_composition_changes(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Tracks composition changes in the index across consecutive days.

        Returns:
            A dictionary where keys are dates and values are lists of composition changes.
            Each change is a dictionary with keys: {'action', 'ticker'}.
        """
        composition_changes = {}
        previous_top_100 = set()

        for date in self.dates:
            # Fetch top 100 stocks for the current date
            current_top_100 = {stock[0] for stock in self.top_100_stocks_provider(date)}

            # Identify additions and removals
            added = current_top_100 - previous_top_100
            removed = previous_top_100 - current_top_100

            changes = [{"action": "Added", "ticker": ticker} for ticker in added] + \
                      [{"action": "Removed", "ticker": ticker} for ticker in removed]

            # Store the changes for the date
            composition_changes[date] = changes
            previous_top_100 = current_top_100

        return composition_changes
