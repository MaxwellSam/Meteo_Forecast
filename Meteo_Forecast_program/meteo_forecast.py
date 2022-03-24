"""
File: meteo_forecast.py
Path: 
Description: meteo_forecast program
Author: Sam Maxwell
Date: 03/2022
"""

# Imports 

import pandas as pd
import os 

## local imports

import modules.variables as var 
import modules.toolbox as tb
import modules.meteo_forecast_classes as forecast

# =============== methods ==============

def load_forecast_api(api_id, station_id):
    if api_id in [api['id'] for api in var.online_api_info]:
        # files path
        path_last_forecast_api = var.path_last_forecast+"{}/{}/".format(api_id, station_id)
        path_archive_api =  var.path_archive+"{}/{}/".format(api_id, station_id)
        # clean dir last forecast
        tb.move_dir_content(path_last_forecast_api, path_archive_api)
        # creat forecast object
        if api_id == "meteoConcept":
            forecast_obj = forecast.MeteoConcept(station_id)
        elif api_id == "openMeteo":
            forecast_obj = forecast.OpenMeteo(station_id)
        forecast_obj.save(path_last_forecast_api)
        return forecast_obj
    else:
        print("Error: API id '{}' not valid 'load_forecast_api(api_id, station_id)'".format(api_id)) 

def load_visualization(list_forecast_obj, station_id):
    # get date forecast 
    path_last_img = var.path_last_forecast+"img/{}/".format(station_id)
    path_archive_img = var.path_archive+"img/{}/".format(station_id)
    # Trace graphs
    graph_temp = forecast.lineChart(list_forecast_obj,"temp")
    graph_precip = forecast.lineChart(list_forecast_obj,"precip")
    graph_etp = forecast.lineChart(list_forecast_obj,"etp")
    # Save graphs
    ## for temp
    tb.move_dir_content(path_last_img+"/temp/", path_archive_img+"/temp/")
    graph_temp.save(path_last_img)
    ## for precip
    tb.move_dir_content(path_last_img+"/precip/", path_archive_img+"/precip/")
    graph_precip.save(path_last_img)
    ## for etp
    tb.move_dir_content(path_last_img+"/etp/", path_archive_img+"/etp/")
    graph_etp.save(path_last_img)

def load_forecasts(station_id):

    # load and save forecast
    list_api_id = [api['id'] for api in var.online_api_info]
    # list_station_id = [station['id'] for station in var.stations_info]
    list_forecast_obj = []
    for api_id in list_api_id:
        forecast_obj = load_forecast_api(api_id, station_id)
        list_forecast_obj.append(forecast_obj)
    # creat and save visualization 
    load_visualization(list_forecast_obj, station_id)

def load_forecasts_all_stations():
    list_stations_id = [station['id'] for station in var.stations_info]
    for station_id in list_stations_id:
        load_forecasts(station_id)

# =============== main ==============

load_forecasts_all_stations()










