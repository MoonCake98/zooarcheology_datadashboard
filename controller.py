import panel as pn
from model import Model_example
from view import View_example

class Controller:
    def __init__(self, model, view):
        """init object with the data model and the constructed panels"""
        self.model = model # data model
        self.view = view # panel panels


    def build_tabs(self):
        """generate the tabs from the panels the view object methods provide"""
        # alert_pandas_version, alert_page1 = self.view.create_alerts() # create a few etst alerts

        # cerate md titles for the tabs
        data_visualisation_page_md_title, \
        geographical_visualisation_page_md_title = \
            self.view.create_markdown_panels()
        column_selection_widget = self.view.create_multichoice_widget()
        # divider = self.view.create_divider_panel()
        # interactive_uniques_distr_panel = self.view.create_interactive_uniques_distribution_plot()

        page1_figure_tabs = pn.Tabs(("unique values",pn.bind(self.view.create_unique_values_fig_panel, columns = column_selection_widget)),
                                    ("n/a values", pn.bind(self.view.create_na_values_fig_panel, columns = column_selection_widget)),
                                    ("unique values per column",self.view.create_dropdown_panel()),
                                    ("dataframe",pn.bind(self.view.create_df_panel, columns = column_selection_widget)),
                                    dynamic = True,
                                    tabs_location = "above")
        # mash together the pane components into pages using the column method
        page1 = pn.Column(data_visualisation_page_md_title,
                        pn.Row(column_selection_widget,page1_figure_tabs))
        # put these columns through the tabs function to generate a tab structure
        tabs = pn.Tabs(("data visualisations", page1),\
                       ("geographical visualisation",
                        self.view.create_page2_column(geographical_visualisation_page_md_title)),
                       dynamic = True)
        return tabs


    def serve(self):
        """serve the contents constructed in build_page"""

        tabs = self.build_tabs()

        # display the tabs
        server = tabs.servable()

        return server


model = Model_example("~/Downloads/f07bce4f-b08c-fe92-6505-c9e534d89a09--v1--full.csv")
view = View_example(model)
controller = Controller(model, view)
controller.serve()
