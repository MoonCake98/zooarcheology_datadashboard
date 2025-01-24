# zooarcheology_dashboards

## intro
This is a project for module 2.2.1 data dashboards. The purpose of this project is the creation and demonstration of a data dashboard.

The dataset I have chosen is a dataset related to zoo archeology from opencontext.org (more about the dataset and where to find it is in the logbook).

## requirements

The tools displayed below have been used for the developement of this dashboard

#### tools
|name|version|
|---|---|
|python|3.11.7|
|pip|23.3.1|

#### python packages

|package name|version|intended use|
|---|---|---|
|panel|1.3.8|the visual construction of our data dashboard and interactive components for the end user|
|pandas|2.1.4|data manipulation (filtering)|
|numpy|1.26.4|calculations on the largescale data|
|folium|0.18.0|geographical interactive map|
|matplotlib.pyplot|3.8.0|general data visualisations|
|seaborn|0.12.2|chronological visualisations|
|plotly|5.9.0|interactive visualisations|


## installation

First off, make sure the required tools are installed, specifically [python](https://www.python.org/downloads/) (version seen in tools) and [pip](https://pip.pypa.io/en/stable/installation/) (version seen in tools).

Follow this up by cloning this repository by executing the command below in your terminal whilst being located in your desired directory.

```bash
git clone https://github.com/MoonCake98/zooarcheology_datadashboard.git
```

Afterwards, to install all the required python packages execute the following command in your terminal:

```bash
pip install -r requirements.txt
```

Lastly, you can run the dashboard by being located in the zooarcheology_datadashboard directory and executing the following command:
```bash
panel serve controller.py
```

Once this is done, the link to the dashboard can be found in your terminal output in the line that is structured like this:
```bash
2025-01-23 5:48:43,910 Bokeh app running at: http://localhost:xxxx/controller
```

If clicking on the link isn't supported in your IDE, then you will have to manually open a browser and navigate towards the address provided in your terminal output by inputting the link into your addres bar in the format of http://localhost:xxxx/controller

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.