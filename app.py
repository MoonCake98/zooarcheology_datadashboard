import pandas as pd

import panel as pn # import panel for ui purposes

# load in all the java extensions etc for the panel server
pn.extension()

dataframe_filepath = "~/Downloads/f07bce4f-b08c-fe92-6505-c9e534d89a09--v1--full.csv"

pn.pane.Alert("render of representation of the dataframe").servable()
pn.pane.Alert("current pandas version " + pd.__version__).servable()



def read_dataframe(dataframe_filepath):
    df = pd.read_csv(dataframe_filepath, low_memory=False)
    return df

# read dataframe
df = read_dataframe(dataframe_filepath)

# display dataframe
pn.pane.DataFrame(df.head()).servable()

#special indicators with dif numbers based on amount
pn.indicators.Number(
    name="Wind Speed",
    value=8.6,
    format="{value} beh",
    colors=[(10, "green"), (100, "red")],
).servable()
