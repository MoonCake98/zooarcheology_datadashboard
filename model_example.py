import pandas as pd


class Model_example:
    def __init__(self, filepath):
        """load in dataset and preprocess some subsets"""
        self.filepath = filepath
        self.df = self.read_dataframe()

    def read_dataframe(self):
        """read dsv file into pandas df"""
        return pd.read_csv(self.filepath, low_memory=False)