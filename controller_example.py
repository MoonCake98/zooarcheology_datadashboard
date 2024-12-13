import panel as pn
from model_example import Model_example
from view_example import View_example

class Controller:
    def __init__(self, model, view):
        """init object with the data model and the constructed panels"""
        self.model = model # data model
        self.view = view # panel panels

    def build_page(self):
        alert_pandas_version, alert_page1 = self.view.create_alerts()
        interactive_map_pane = self.view.create_map()
        page = pn.Column(alert_pandas_version, alert_page1,interactive_map_pane)
        return page


    def serve(self):
        """serve the contents constructed in build_page"""
        page = self.build_page()
        page.servable()

model = Model_example("~/Downloads/f07bce4f-b08c-fe92-6505-c9e534d89a09--v1--full.csv")
view = View_example(model)
controller = Controller(model, view)
controller.serve()
