import pandas as pd

import panel as pn # import panel for ui purposes



def display_alert_panel(alert_string):
    pn.pane.Alert(alert_string).servable()
    return

def display_dataframe(pandas_dataframe):
    pn.pane.DataFrame(pandas_dataframe).servable()
    return


def read_dataframe(dataframe_filepath):
    dataframe = pd.read_csv(dataframe_filepath, low_memory=False)
    return dataframe

def main():

    # load in all the java extensions etc for the panel server
    pn.extension()
    dataframe_filepath = "~/Downloads/open-context-24296-records(1).csv"
    dataframe = read_dataframe(dataframe_filepath)
    display_alert_panel("This is a redner of my dataframe in panel")

    display_dataframe(dataframe)

    return

if __name__ == "__main__":
    main()


# test
# pn.indicators.Number(
#     name="Wind Speed",
#     value=8.6,
#     format="{value} non nan",
#     colors=[(10, "green"), (100, "red")],
# ).servable()
