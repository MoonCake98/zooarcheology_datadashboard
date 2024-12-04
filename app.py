import pandas as pd # import pandas for data handling purposes

import panel as pn # import panel for ui purposes
# panel run command: panel serve app.py --dev


# load in all the java extensions etc for the panel server
pn.extension()

# make 2 alert pane objects 
pan2 = pn.pane.Alert("current pandas version " + pd.__version__)
pan1 = pn.pane.Alert("render of representation of the dataframe")

# define data file path
dataframe_filepath = "~/Downloads/f07bce4f-b08c-fe92-6505-c9e534d89a09--v1--full.csv"

# define data reading function
def read_dataframe(df_filepath):
    """reading in of the datafile into a pandas dataframe"""
    df = pd.read_csv(df_filepath, low_memory=False)
    return df

# read dataframe
df = read_dataframe(dataframe_filepath)

# select head and collumns with variables of interest of the dataframe to avoid visual clutter and display this
df_display_head_panel = pn.pane.DataFrame(df[df.columns[[1,2,4,6,7,8,26,27]]].head())

# filter the df for unique coordinates of the dataset and display this
df_unique_coordinates = pn.pane.DataFrame(pd.DataFrame(df[df.columns[[7, 8]]].drop_duplicates()))

# put the 2 dataframes on a single row
df_row = pn.Row(df_display_head_panel,df_unique_coordinates)
full_page_collumn = pn.Column(pan1,pan2,df_row).servable()
