import pandas as pd # import pandas for data handling purposes

import panel as pn # import panel for ui purposes


# load in all the java extensions etc for the panel server
pn.extension()

# define data file path
dataframe_filepath = "~/Downloads/f07bce4f-b08c-fe92-6505-c9e534d89a09--v1--full.csv"

# define data reading function
def read_dataframe(df_filepath):
    """reading in of the datafile into a pandas dataframe"""
    df = pd.read_csv(df_filepath, low_memory=False)
    return df

# read dataframe
df = read_dataframe(dataframe_filepath)

#select collumns with variables of interest of the dataframe to avoid visual clutter
display_df = df[df.columns[[1,2,4,6,7,8,26,27]]]


# display head of dataframe to get a visualisation of the dataframe
df_pane = pn.pane.DataFrame(display_df.head())

