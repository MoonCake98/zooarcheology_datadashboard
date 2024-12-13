import pandas as pd


class Model_example:
    def __init__(self, filepath):
        """load in dataset and preprocess some subsets"""
        self.filepath = filepath
        self.df = self.read_dataframe()
        self.unique_coordinates_df = self.get_unique_coordinates()
        self.mean_coordinates = self.unique_coordinates_df.mean()

    def get_unique_coordinates(self):
        """get unique coords from dataset"""
        return self.df[self.df.columns[[7, 8]]].drop_duplicates()


    def read_dataframe(self):
        """read dsv file into pandas df"""
        return pd.read_csv(self.filepath, low_memory=False)