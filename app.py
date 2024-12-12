import pandas as pd # import pandas for data handling purposes

import panel as pn # import panel for ui purposes
# panel run command: panel serve app.py --dev

import numpy as np

import folium as fl

import matplotlib.pyplot as plt


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
unique_coordinates_df = df[df.columns[[7, 8]]].drop_duplicates()
df_unique_coordinates_panel = pn.pane.DataFrame(unique_coordinates_df)

# create the mean dataframe and panel
mean_df = pd.DataFrame(unique_coordinates_df.mean()).transpose()

mean_panel = pn.pane.DataFrame(mean_df)

# put 3 dataframes into a single row
df_row = pn.Row(pn.Column(df_display_head_panel,mean_panel),df_unique_coordinates_panel)

## create a map to represent the 15 different coordinates found in the dataset
# map centered on the mean of all the unique coordinates in the data
coordinate_map = fl.Map(location=[mean_df["Latitude (WGS-84)"], mean_df["Longitude (WGS-84)"]], zoom_start=12)
interactive_map_panel = pn.pane.plot.Folium(coordinate_map, height=400)

# for loop to put markers corresponding to the 15 unique locations ontto the map
for latitude, longititude,project in zip(unique_coordinates_df["Latitude (WGS-84)"],
                                unique_coordinates_df["Longitude (WGS-84)"],
                                df.loc[unique_coordinates_df.index]["Project"]):
    fl.Marker([latitude,longititude],popup=project,tooltip="click for project").add_to(coordinate_map)

# update map panel to include these markers
interactive_map_panel.object = coordinate_map


## generate plot to showcase unique value distribution amongst columns of the dataframe
# filter the dataframe for uniques
df_uniques = df.nunique()

# generate plot figure
plt.figure(figsize=(15, 8))
df_uniques.plot(kind='bar', color='skyblue', edgecolor='black')

# plot labels
plt.xlabel("Columns")
plt.ylabel("Number of Unique Values")
plt.title("Unique Values per Column")

# plot column label distances and orientation
plt.xticks(ticks=range(len(df_uniques.index)),ha="right",va="top", labels=df_uniques.index,rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# add a line ot show the total amount of rows
plt.axhline(y=239320, color='red', linestyle='--', linewidth=2, label='total row amount')

# log plot cause very broad value range
plt.yscale('log')

# add legend
plt.legend()

# avoid overlap
plt.tight_layout()

unique_plot_pane = pn.pane.Matplotlib(plt.gcf(), dpi=100)

## plot to show the na's and not na's per column
# Sample function to count N/A-like values and actual values per column
def count_na_and_values(df):
    na_counts = {}
    actual_counts = {}
    
    for column in df.columns:
        # Count the number of NaN or N/A-like values (e.g., 'NaN', 'N/A', 'unknown')
        na_count = df[column].isna().sum() + df[column].isin(['NaN', 'N/A', 'unknown']).sum()
        # Count the number of actual values (non-NaN and non-N/A-like)
        actual_count = len(df[column]) - na_count
        
        na_counts[column] = na_count
        actual_counts[column] = actual_count
    
    return na_counts, actual_counts

# Calculate counts
na_counts, actual_counts = count_na_and_values(df)

# Plotting the bar chart with two segments for each column
fig, ax = plt.subplots(figsize=(15, 8))
bar_width = 0.6  # Width of the bars
index = np.arange(len(df.columns))  # Position of the bars

# Plot N/A-like values as one part of the bar (in red)
bars1 = ax.bar(index, na_counts.values(), bar_width, color='red', label='N/A-like Values')

# Plot actual values as another part of the bar (in blue)
bars2 = ax.bar(index, actual_counts.values(), bar_width, bottom=list(na_counts.values()), color='blue', label='Actual Values')

# Plot labels
ax.set_xlabel("Columns")
ax.set_ylabel("Number of Values")
ax.set_title("Distribution of N/A-like and Actual Values per Column")
ax.set_xticks(index)
ax.set_xticklabels(df.columns, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
na_distr_plot_pane = pn.pane.Matplotlib(plt.gcf(), dpi=100)

## unique values dropdown interactive df
# Function to create a DataFrame of unique values for a given column
def get_unique_values_df(selected_col):
    unique_values = pd.Series(df[selected_col].unique())
    return pn.pane.DataFrame(unique_values, name=selected_col, width=400)

# Create a dropdown menu to select a column from the DataFrame (using Select)
dropdown = pn.widgets.Select(name='Select Column, to display unique values', options=list(df.columns))

# Panel to update the displayed DataFrame based on the dropdown selection
interactive_panel = pn.bind(get_unique_values_df, selected_col=dropdown)

# Display the dropdown and the interactive panel
interactive_uniques_per_column_panel = pn.Column(dropdown, interactive_panel)


# put the contents of the above elemnts into a column to get a single object for the whole first page
fullpage1_collumn = pn.Column(alert_panel_text_page1,alert_panel_pandasversion,df_row,unique_plot_pane,na_distr_plot_pane)

# make placeholder alert and markdown title panel for future geographical visualisation
markdown_panel_title_page2 = pn.pane.Markdown("# geographical visualisation")
alert_panel_text_page2 = pn.pane.Alert("ask about marker clustering plugin (https://python-visualization.github.io/folium/latest/user_guide/plugins/marker_cluster.html)")

# add placeholders together into a column to get a single object for the second page
fullpage2_collumn = pn.Column(markdown_panel_title_page2, alert_panel_text_page2,interactive_map_panel,interactive_uniques_per_column_panel)

# add tabs so I can seperated the fd representations and the future geographical visualisation
tabs = pn.Tabs(
    ("dataframe visualisation", fullpage1_collumn),  # Title and content for each tab
    ("coordinate grapical representation", fullpage2_collumn)
)





tabs.servable()
