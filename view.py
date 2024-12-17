import panel as pn
import folium as fl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from folium.plugins import MarkerCluster

class View_example:
    def __init__(self, model):
        """initialise view object with the model data as a self property"""

        self.model = model
        return


    def create_alerts(self):
        """create confirmed working alerts (tested in app.py)"""

        alert_pandas_version = pn.pane.Alert(f"Current pandas version: {pd.__version__}")
        alert_page1 = pn.pane.Alert("Representation of the dataframe")

        return alert_pandas_version, alert_page1


    def create_map(self):
        """create interactive map with markers centered on the mean of all unique coordinates"""

        mean_coords = self.model.mean_coordinates 

        coord_map = fl.Map(location=[mean_coords["Latitude (WGS-84)"], mean_coords["Longitude (WGS-84)"]], zoom_start=6)

        # for loop for generating markers on all the unique coords
        # has to be done like this because you can only create one marker at a time
        for lat, lng, project in zip(
            self.model.unique_coordinates_df["Latitude (WGS-84)"],
            self.model.unique_coordinates_df["Longitude (WGS-84)"],
            self.model.df.loc[self.model.unique_coordinates_df.index]["Project"]
        ):
            fl.Marker([lat, lng], popup=project, tooltip="Click for project").add_to(coord_map)
            

        return pn.pane.plot.Folium(coord_map, height=400)
    

    def create_static_plots(self):
        """create plots for unique values and N/A- value distribution"""

        # Unique values plot
        unique_counts = self.model.df.nunique()
        plt.figure(figsize=(15, 8))
        unique_counts.plot(kind='bar', color='steelblue')
        plt.xlabel("Columns")
        plt.ylabel("Number of Unique Values")
        plt.title("Unique Values per Column")
        plt.xticks(ticks=range(len(unique_counts.index)), ha="right", va="top", labels=unique_counts.index, rotation=45)
        plt.yscale('log')
        plt.axhline(y=239320, color='red', linestyle='--', linewidth=2, label='Total Rows')
        plt.legend()
        txt="I need the caption to be present a little below X-axis"
        plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        unique_values_plot = pn.pane.Matplotlib(plt.gcf(), dpi=100)

        # N/A-ish values distribution
        na_counts, actual_counts = self.model.count_na_and_actual_values()
        fig, ax = plt.subplots(figsize=(15, 8))
        index = np.arange(len(na_counts))
        ax.bar(index, na_counts.values(), label='N/A-like Values', color='salmon')
        ax.bar(index, actual_counts.values(), bottom=list(na_counts.values()), label='Actual Values', color='steelblue')
        ax.set_xticks(index)
        ax.set_xticklabels(self.model.df.columns ,ha="right" ,va="top" ,rotation=45)
        ax.set_title("N/A-like vs Actual Values per Column")
        plt.legend()
        plt.tight_layout()
        # background_color = "#213635"
        # fig.patch.set_facecolor(background_color)  # background color for the figure
        # ax.set_facecolor(background_color)  # background color for the axes
        na_values_plot = pn.pane.Matplotlib(plt.gcf(), dpi=100)

        return unique_values_plot, na_values_plot
    

    def create_dropdown_panel(self):
        """create an interactive dropdown to display unique values per column"""

        dropdown = pn.widgets.Select(name="Select Column to Display Unique Values", options=list(self.model.df.columns))
        dropdown.value = "Project"
        panel = pn.bind(lambda col: pn.pane.DataFrame(pd.Series(self.model.get_column_unique_values(col))), col=dropdown)
        return pn.Column(dropdown, panel)
    

    def create_markdown_panels(self):
        """create some markdown panels to use in the pages for context"""

        data_visualisation_page_md_title = pn.pane.Markdown("# data visualisations\n---")
        geographical_visualisation_page_md_title = pn.pane.Markdown("# geographical visualisation\n---")
        return data_visualisation_page_md_title,geographical_visualisation_page_md_title
    

    def create_divider_panel(self):
        return pn.layout.Divider(sizing_mode='stretch_width')
    

    def create_df_head_panel(self,columns):
        # columns ia redundant for now because I plan to implement filtering in the future
        return self.model.df.head()