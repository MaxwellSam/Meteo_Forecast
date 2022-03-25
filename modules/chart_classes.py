"""
File: chart_classes.py
Path: ./modules/chart_classes.py
Description: Classes for visualization and API comparison
Author: Sam Maxwell
Date: 03/2022
"""

# Imports

import plotly.graph_objects as go

# =============================== Classes ================================== #

class lineChart:
    """
    Class for line chart visualization of meteorological parameters evolution for different APIs.
    
    Initialisation parameters:
        forecast_obj_list       List of forecast object to get trace and informations
                                type: `list<forecast objects>`
        param                   Meteorological parameters to get traces
                                type: `string` 

    Attributs:
        date            Forecast date
                        type: `string`
        station_id      Hourly forecast Dataframe
                        type: `pandas Dataframe object`
    
    Methods: 
        save(path)                  Save graphic as png. 
    """

    def __init__(self, forecast_obj_list, param):
        # get info forecast
        self.date = forecast_obj_list[0].date_init
        self.station_id = forecast_obj_list[0].station_info['id']
        # save info
        self.param = param
        # init figure
        self.fig = go.Figure(
            layout=go.Layout(
                title=go.layout.Title(text="Evolution of "+param)
            )
        )
        # generate traces
        list_trace = []
        for obj in forecast_obj_list:
            list_trace.extend(obj.trace(param))

        # add traces to figure
        for trace in list_trace:
            self.fig = self.fig.add_trace(go.Scatter(
                x = trace["x"],
                y = trace["y"],
                name = trace["name"]
            ))
        self.fig.update_xaxes(title_text='date')
        self.fig.update_yaxes(title_text=param)
    
    def save(self, path):
        f_name = "{}_{}_{}.png".format(self.param, self.station_id, self.date) 
        path += "{}/{}".format(self.param, f_name) 
        print("# Save file '{}' ... ".format(f_name), end="") 
        self.fig.write_image(path)
        print("Done")
