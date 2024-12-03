import pandas as pd

class IndexConstructor:
    """
    Constructs an equal-weighted custom index.
    """
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_top_100(self, date):
        """
        Retrieves the top 100 stocks by market cap for a given date.
        """
        query = """
            SELECT ticker, price, market_cap
            FROM stock_data
            WHERE date = ?
            ORDER BY market_cap DESC
            LIMIT 100
        """
        return self.db_manager.query(query, (date,))

    def build_index(self, dates):
        """
        Builds an equal-weighted index over the given dates.
        """
        index_values = []
        previous_top_100 = set()
        composition_changes = []

        for date in dates:
            top_100 = self.get_top_100(date)
            weight = 1 / 100
            index_value = sum(row[1] * weight for row in top_100)
            index_values.append({"date": date, "index_value": index_value})

            current_top_100 = {row[0] for row in top_100}
            added = current_top_100 - previous_top_100
            removed = previous_top_100 - current_top_100
            composition_changes.append({"date": date, "added": list(added), "removed": list(removed)})

            previous_top_100 = current_top_100

        return pd.DataFrame(index_values), composition_changes
