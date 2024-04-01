import pandas as pd

class GenericScraper:
    def __init__(self, source):
        self.source = source

    def process_data(self, data):
        """
        Convert collected data into a DataFrame, add 'Source' column,
        and set the DataFrame index.
        """
        df = pd.DataFrame(data)
        df["Source"] = self.source
        df.index = df["Source"] + df['Number'].astype(str)
        df.index.name = None
        return df