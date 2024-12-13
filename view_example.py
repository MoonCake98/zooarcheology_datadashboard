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