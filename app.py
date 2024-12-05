import pandas as pd # import pandas for data handling purposes

import panel as pn # import panel for ui purposes
# panel run command: panel serve app.py --dev

import folium as fl


# load in all the java extensions etc for the panel server
pn.extension()

# make 2 alert pane objects
alert_panel_pandasversion = pn.pane.Alert("current pandas version " + pd.__version__)
alert_panel_text_page1 = pn.pane.Alert("representation of the dataframe")

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
df_unique_coordinates_panel = pn.pane.DataFrame(pd.DataFrame(df[df.columns[[7, 8]]].drop_duplicates()))

mean_df = pd.DataFrame(df[df.columns[[7, 8]]].drop_duplicates().mean()).transpose()


pd.DataFrame({})

mean_panel = pd.DataFrame(mean_df)





# put the 2 dataframes on a single row
df_row = pn.Row(pn.Column(df_display_head_panel,mean_panel),df_unique_coordinates_panel,mean_panel)

# m = fl.Map(location=[mean_df["Latitude (WGS-84)"], mean_df["Longitude (WGS-84)"]], zoom_start=12)

# folium_pane = pn.pane.plot.Folium(m, height=400)


# put the contents of the above elemnts into a column to get a single object for the whole first page
fullpage1_collumn = pn.Column(alert_panel_text_page1,alert_panel_pandasversion,df_row)

# make placeholder alert and markdown title panel for future geographical visualisation
markdown_panel_title_page2 = pn.pane.Markdown("# future geographical visualisation")
alert_panel_text_page2 = pn.pane.Alert("this is simply a placeholder, the actual figure has yet to be finished")

# add placeholders together into a column to get a single object for the second page
fullpage2_collumn = pn.Column(markdown_panel_title_page2, alert_panel_text_page2)

# add tabs so I can seperated the fd representations and the future geographical visualisation
tabs = pn.Tabs(
    ("dataframe visualisation", fullpage1_collumn),  # Title and content for each tab
    ("coordinate grapical representation", fullpage2_collumn)
)





tabs.servable()
