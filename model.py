import pandas as pd


class Model_example:
    def __init__(self, filepath):
        """load in dataset and preprocess some subsets"""

        self.filepath = filepath # define the filepath as a property of the object

        self.df = self.read_dataframe() # read in the data corresponding to the previously provided filepath

        self.unique_coordinates_df = self.get_unique_coordinates()

        self.mean_coordinates = self.unique_coordinates_df.mean() # get the mean of the unique coords to get a map starting point

    def get_unique_coordinates(self):
        """get unique coords from dataset columns 7 and 8"""
        return self.df[self.df.columns[[7, 8]]].drop_duplicates()


    def read_dataframe(self):
        """read dsv file into pandas df"""
        # note that the pandas read fucniton has to be called with the low_memory variable as False
        # this is because of the size of the dataset
        return pd.read_csv(self.filepath, low_memory=False)