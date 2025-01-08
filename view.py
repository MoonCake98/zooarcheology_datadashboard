import panel as pn
import panel.widgets as wdgts
import folium as fl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from folium.plugins import MarkerCluster


class View_example:
    def __init__(self, model):
        """initialise view object with the model data as a self property"""

        self.model = model
        pn.extension('tabulator')
        return


    def create_alerts(self):
        """create confirmed working alerts (tested in app.py)"""

        alert_pandas_version = pn.pane.Alert(f"Current pandas version: {pd.__version__}")
        alert_page1 = pn.pane.Alert("Representation of the dataframe")

        return alert_pandas_version, alert_page1


    def create_map(self):
        """create interactive map with markers centered on the mean of all unique coordinates"""
        coord_map = fl.Map(location=[self.model.mean_coordinates ["Latitude (WGS-84)"],
                                     self.model.mean_coordinates ["Longitude (WGS-84)"]], zoom_start=6)

        marker_cluster = MarkerCluster().add_to(coord_map)

        # for loop for generating markers on all the unique coords
        # has to be done like this because you can only create one marker at a time
        for lat, lng, project in zip(
            self.model.unique_coordinates_df["Latitude (WGS-84)"],
            self.model.unique_coordinates_df["Longitude (WGS-84)"],
            self.model.df.loc[self.model.unique_coordinates_df.index]["Project"]
        ):
            fl.Marker([lat, lng], popup=project, tooltip="Click for project").add_to(marker_cluster)
            

        return pn.pane.plot.Folium(coord_map, height=400)
    

    def create_unique_values_fig_panel(self, columns):
        """create a plot for unique values distributed over the dataframe"""
        unique_counts = self.model.get_subset_df(columns).nunique()
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
        return pn.pane.Matplotlib(plt.gcf(), dpi=100)


    def create_na_values_fig_panel(self, columns):
        """create plot N/A- value distribution"""

        # N/A-ish values distribution
        filtered_df = self.model.get_subset_df(columns)
        na_counts, actual_counts = self.model.count_na_and_actual_values(df=filtered_df, columns= columns)
        fig, ax = plt.subplots(figsize=(15, 8))
        index = np.arange(len(na_counts))
        ax.bar(index, na_counts.values(), label='N/A-like Values', color='salmon')
        ax.bar(index, actual_counts.values(), bottom=list(na_counts.values()), label='Actual Values', color='steelblue')
        ax.set_xticks(index)
        ax.set_xticklabels(columns ,ha="right" ,va="top" ,rotation=45)
        ax.set_title("N/A-like vs Actual Values per Column")
        plt.legend()
        plt.tight_layout()
        # background_color = "#213635"
        # fig.patch.set_facecolor(background_color)  # background color for the figure
        # ax.set_facecolor(background_color)  # background color for the axes

        return pn.pane.Matplotlib(plt.gcf(), dpi=100)
    
    def create_column_dropdown_widget(self):
        """create a dropdown menu to select a column out of the all available ones"""
        return pn.widgets.Select(name="select a column for it's unqiue values",
                                 options=list(self.model.df.columns),
                                 value="Project")

    def create_dropdown_panel(self):
        """create an interactive dropdown to display unique values per column"""

        dropdown = create_column_dropdown_widget()
        dropdown.value = "Project"
        panel = pn.bind(lambda col: pn.widgets.Tabulator(pd.DataFrame(pd.Series(self.model.get_column_unique_values_subset(col))),pagination='remote', page_size=20), col=dropdown)
        return pn.Column(dropdown, panel)
    

    def create_markdown_panels(self):
        """create some markdown panels to use in the pages for context"""

        data_visualisation_page_md_title = pn.pane.Markdown("# data visualisations\n---")
        geographical_visualisation_page_md_title = pn.pane.Markdown("# geographical visualisation\n---")
        row_filter_md_title_and_description = pn.pane.Markdown(
            "# filter row values\n---\nselect the values of the rows you want to filter the data on")
        return data_visualisation_page_md_title, geographical_visualisation_page_md_title, row_filter_md_title_and_description
    

    def create_divider_panel(self):
        """create a divider panel so we can clearly indicate sections of a page"""
        return pn.layout.Divider(sizing_mode='stretch_width')
    

    def create_df_panel(self,columns):
        # columns is redundant for now because I plan to implement filtering in the future
        return pn.widgets.Tabulator(self.model.get_subset_df(columns), pagination='remote', page_size=20)
    

    def create_page2_column(self,title_md_panel):
        """
        generate a column containing the contyents of page 2,
        this is a funciton in view so we don't have to 
        load in the page until we switch to the relevant tab
        """
        return pn.Column(title_md_panel,
                         self.create_map())


    def create_multichoice_widget(self):
        """create a widget for filtering columns in panel test"""

        return pn.widgets.MultiChoice(name = "select columns to keep",
                                     options=list(self.model.df.columns),
                                     value = [self.model.df.columns[1],
                                              self.model.df.columns[2],
                                              self.model.df.columns[4],
                                              self.model.df.columns[6],
                                              self.model.df.columns[7],
                                              self.model.df.columns[8],
                                              self.model.df.columns[10],
                                              self.model.df.columns[11]
                                     ]
                                     )
    
    def create_column_dropdown_widget(self):
        """create a dropdown menu to select a column out of the all available ones"""
        return pn.widgets.Select(name="select a column for it's unqiue values",
                                 options=list(self.model.df.columns),
                                 value="Project")
    
    def create_row_value_filter_multichoice_widget(self, column="Project"):
        """create a widget for the purposes of filtering the dataset based on row values"""

        return pn.widgets.MultiChoice(name = "select values to filter on",
                                      options = self.model.get_unique_values_per_column_list(column))
