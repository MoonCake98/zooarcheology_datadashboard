import pandas as pd

class Model_example:
    def __init__(self, filepath:str):
        """load in dataset and preprocess some subsets"""

        self.filepath = filepath # define the filepath as a property of the object

        self.df = self.read_dataframe() # read in the data corresponding to the previously provided filepath\
        
        self.fdf = self.df.copy()

        self.unique_coordinates_df = self.get_unique_coordinates()

        self.mean_coordinates = self.unique_coordinates_df.mean() # get the mean of the unique coords to get a map starting point


    def get_unique_coordinates(self) -> pd.DataFrame:
        """get unique coords from dataset columns 7 and 8"""
        return self.df[self.df.columns[[7, 8]]].drop_duplicates()


    def read_dataframe(self) -> pd.DataFrame:
        """read csv file into pandas df"""
        # note that the pandas read fucniton has to be called with the low_memory variable as False
        # this is because of the size of the dataset
        return pd.read_csv(self.filepath, low_memory=False)


    def get_column_unique_values_subset(self, column:str) -> pd.Series :
        """get unique values from a specific column"""
        return self.get_subset_df(column).unique()


    def count_na_and_actual_values(self, df: pd.DataFrame, columns:list) -> pd.DataFrame:
        """calculate counts of N/A-like and actual values for each column"""
        na_counts = {}
        actual_counts = {}

        for column in columns:
            na_count = df[column].isna().sum() + df[column].isin([
                'NaN', 'N/A', 'unknown', "indeterminate", "nan",
                "Best available location data", 
                "Area Not recorded", "Level ?",
                  "Area [Not indicated]","Bag  Not recorded",
                  "Bag  383?", "Level Not recorded","NaN",
                  "Strat Group [??]", "Strat Group [?]",
                  "Strat Group [???]", "(Context Unknown)", 
                  "Unit [Not indicated]"]).sum()
            actual_count = len(df[column]) - na_count
            na_counts[column] = na_count
            actual_counts[column] = actual_count

        return na_counts, actual_counts
    
    def get_subset_df(self,columns:list) -> pd.DataFrame:
        """get a subset of the dataframe with only the columns provided as arguments"""
        return self.df[columns]
    
    def get_unique_values_per_column_list(self,column:str) -> list:
        """returns a list of unique values within the submitted column"""
        return list(self.df[column].drop_duplicates())
    
    def filter_dataframe_values(self, df:pd.DataFrame, values:list):
        """returns a subset of a dataframe where only the rows"""
        return
    
    def update_fdf(self, columns:list, values:list) -> pd.DataFrame:
        """updates the filtered dataframe to the selected columns and values"""
        self.fdf = self.get_subset_df(columns)

    