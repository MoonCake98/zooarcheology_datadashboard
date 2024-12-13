import panel as pn
import folium as fl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    