import panel as pn
import panel.widgets as wdgts
import folium as fl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
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
        plt.close('all') # close all previous figures
        """create a plot for unique values distributed over the dataframe"""

        unique_counts = self.model.get_subset_df(columns).nunique()
        plt.figure(figsize=(15, 8))
        unique_counts.plot(kind='bar', color='steelblue')
        plt.xlabel("Columns")
        plt.ylabel("Number of Unique Values")
        plt.title("Unique Values per Column")
        plt.xticks(ticks=range(len(unique_counts.index)),
                    ha="right",
                      va="top",
                        labels=unique_counts.index,
                          rotation=45)
        plt.yscale('log')
        plt.axhline(y=239320, color='red', linestyle='--', linewidth=2, label='Total Rows')
        # add labels to indicate the hard numbers if the bars
        for bar_index, value in enumerate(unique_counts):
            plt.text(
                x=bar_index, y=value - (value*0.35), s=str(value), ha='center', va='bottom', fontsize=10, color="white"
                    )
        plt.legend()
        txt="I need the caption to be present a little below X-axis"
        plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        return pn.pane.Matplotlib(plt.gcf(), dpi=100)


    def create_na_values_fig_panel(self, columns):
        """create plot N/A- value distribution"""
        plt.close('all') # close all previous figures


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

        # add labels to indicate the hard numbers if the bars
        for bar_index, (na, actual) in enumerate(zip(na_counts.values(), actual_counts.values())):
            ax.text(
                x=bar_index, y=na / 2, s=str(na), ha='center', va='center', fontsize=10, color='black'
            )
            ax.text(
                x=bar_index, y=na + actual / 2, s=str(actual), ha='center', va='center', fontsize=10, color='white'
            )
        plt.tight_layout()
        # background_color = "#213635"
        # fig.patch.set_facecolor(background_color)  # background color for the figure
        # ax.set_facecolor(background_color)  # background color for the axes

        return pn.pane.Matplotlib(plt.gcf(), dpi=100)
    
    # def create_unique_distribution_fig_panel(self, columns):
    #         """create a figure to show the distribution of unique values in the dataset"""



    
    def create_column_dropdown_widget(self):
        """create a dropdown menu to select a column out of the all available ones"""
        return pn.widgets.Select(name="select a column for its unqiue values",
                                 options=list(self.model.df.columns),
                                 value="Project")

    def create_dropdown_row(self):
        """create an interactive dropdown to display unique values per column"""

        dropdown = self.create_column_dropdown_widget()
        dropdown.value = "Project"
        panel = pn.bind(lambda col: pn.widgets.Tabulator(pd.DataFrame(pd.Series(self.model.get_column_unique_values_subset(col))),
                                                         pagination='remote', page_size=20), col=dropdown)
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
        """create a panel to display the dataframe"""
        tabulated_df = pn.widgets.Tabulator(self.model.get_subset_df(columns), pagination='remote', page_size=20)
        # filename, download_button = tabulated_df.download_menu(
        # text_kwargs={'name': 'Enter filename', 'value': 'placeholder.csv'},
        # button_kwargs={'name': 'Download table'}
        # )
        return tabulated_df #, filename, download_button
    

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

    
    def create_row_value_filter_multichoice_widget(self, column):
        """create a widget for the purposes of filtering the dataset based on row values"""

        return pn.widgets.Select(name = "select values to filter on",
                                      options = self.model.get_unique_values_per_column_list(column))

    def create_row_value_filter_combination_row(self):
        """returns a panel row containing a dropdown menu containing the available columns and
         a multichoice panel whose options are based upon the previously mentioned dropdown menu"""
        dropdown_column_menu = self.create_column_dropdown_widget()
        multichoice_panel = pn.bind(self.create_row_value_filter_multichoice_widget,
                column = dropdown_column_menu)
        return dropdown_column_menu, multichoice_panel
    
    
    def test_alerts(self):
        """create a test alert to confirm the working functionality of the pregenerated mask dict"""
        return pn.pane.Alert(f"{self.model.pre_gen_mask_dict.keys()}")
    
    def create_multichoice_applied_filters_widget(self):
        """create a multichoice panel for the purposes of displaying currently applied filters"""
        return pn.widgets.MultiChoice(name="currently selected filters",
                                      options = list(self.model.unique_val_col_dict.keys()))
    
    def create_distributions_durations_figure(self, columns):
        """createa a plot to show the distribution of the durations in the dataset with a bar and line plot"""

        plt.close('all') # close all previous figures

        df = self.model.get_subset_df(columns)

        # calculate duration
        df['duration'] = df['Late Date (BCE/CE)'] - df['Early Date (BCE/CE)']

        # plot histogram
        sns.histplot(df['duration'], bins=10, kde=True)
        plt.title('Distribution of Durations (Years)')
        plt.xlabel('Duration (Years)')
        plt.ylabel('Frequency')
        plt.show()


        return pn.pane.Matplotlib(plt.gcf(), dpi=100)
    
    def create_heatmap_figure(self, columns):
        """create heatmap of periods of late and early in 100 year intervals"""
        plt.close('all') # close all previous figures

        df = self.model.get_subset_df(columns)

        # divide dates into 100year intervals
        df['Early Century'] = (df['Early Date (BCE/CE)'] // 100).astype(int) * 100
        df['Late Century'] = (df['Late Date (BCE/CE)'] // 100).astype(int) * 100

        # count events by centuries
        counts = df.groupby(['Early Century', 'Late Century']).size().reset_index(name='count')

        # pivot table for heatmap
        heatmap_data = counts.pivot_table(index='Early Century', columns='Late Century', values='count', fill_value=0)

        # slot the heatmap
        sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt="d")

        # set the title and labels
        plt.suptitle('Event Counts by Century (BCE/CE) figure 4', fontsize=16, y=1.05)
        plt.xlabel('Late Century')
        plt.ylabel('Early Century')

        # invert the Y-axis so that the century starts from 0 at the top
        plt.gca().invert_yaxis()

        # set the limits of the Y-axis explicitly, if necessary
        plt.gca().set_ylim(heatmap_data.index.max() + 1, heatmap_data.index.min() - 1)


        return pn.pane.Matplotlib(plt.gcf(), dpi=100)

    def create_scatterplot_figure(self, columns):
        """create scatter plot to show distribution of late and early dates"""
        plt.close('all') # close all previous figures

        df = self.model.get_subset_df(columns)

        sns.scatterplot(
            x='Early Date (BCE/CE)',
            y='Late Date (BCE/CE)',
            data=df
        )
        plt.axhline(0, color='gray', linestyle='--', label='Start of CE (Y=0)')
        plt.axvline(0, color='gray', linestyle='--', label='Start of CE (X=0)')
        plt.title('Early Date vs Late Date (fig 5)')
        plt.xlabel('Early Date (BCE/CE)')
        plt.ylabel('Late Date (BCE/CE)')
        plt.legend()

        return pn.pane.Matplotlib(plt.gcf(), dpi=100)
    
    
