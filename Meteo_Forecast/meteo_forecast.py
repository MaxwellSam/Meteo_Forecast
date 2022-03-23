"""
File: meteo_forecast.py
Path: 
Description: meteo_forecast program
Author: Sam Maxwell
Date: 03/2022
"""

# Imports 

import pandas as pd

## local imports

import modules.variables as var 
import modules.toolbox as tb
import modules.meteo_forecast_classes as forecast

# =============== main method ==============

def load_forecasts(station_id):
    """
    Load OpenMeteo and MeteoConcept forecasts, save data and visualisations. 
    """
    # clean dir last forecast
    tb.move_dir_content(var.path_last_forecast+"openMeteo/", var.path_archive+"openMeteo")
    tb.move_dir_content(var.path_last_forecast+"meteoConcept/", var.path_archive+"meteoConcept/")
    # Forecast classes
    meteoConcept = forecast.MeteoConcept(station_id)
    openMeteo = forecast.OpenMeteo(station_id)
    # Save forecasts
    openMeteo.save(var.path_last_forecast+"openMeteo/")
    meteoConcept.save(var.path_last_forecast+"meteoConcept/")
    # Trace graphs
    graph_temp = forecast.lineChart([openMeteo, meteoConcept],"temp")
    graph_precip = forecast.lineChart([openMeteo, meteoConcept],"precip")
    graph_etp = forecast.lineChart([openMeteo, meteoConcept],"etp")
    # Save graphs
    graph_temp.fig.write_image(var.path_images+"temp.png")
    graph_precip.fig.write_image(var.path_images+"precip.png")
    graph_etp.fig.write_image(var.path_images+"etp.png")

# --------------- load forecast -----------------

load_forecasts("BrenneBrain")










