"""
File: meteo_forecast.py
Path: ./meteo_forecast.py 
Description: Meteo Forecast program file.
             Containe methods for meteo forecast recovery automation with archiving system.
Author: Sam Maxwell
Date: 03/2022
"""

# Imports 

## local imports

import modules.variables as var 
import modules.toolbox as tb
import modules.meteo_forecast_classes as forecast
import modules.chart_classes as chart

# =============== methods ==============

def load_forecast_api(api_id, station):
    """
    Load forecast from online API, move last forecast to archive and save new forecast in last forecast for a sation. 
    
    Parameters:
        api_id      ID of online api to request
                    type: str
        station     informations of station to get forecast
                    type: dict    
    """
    if api_id in [api['id'] for api in var.online_api_info]:
        # files path
        path_last_forecast_api = var.path_last_forecast+"{}/{}/{}/".format(api_id, station["zone"],station["id"])
        path_archive_api =  var.path_archive+"{}/{}/{}/".format(api_id, station["zone"], station["id"])
        # clean dir last forecast
        tb.move_dir_content(path_last_forecast_api, path_archive_api)
        # creat forecast object
        if api_id == "meteoConcept":
            forecast_obj = forecast.MeteoConcept(station["id"])
        elif api_id == "openMeteo":
            forecast_obj = forecast.OpenMeteo(station["id"])
        forecast_obj.save(path_last_forecast_api)
        return forecast_obj
    else:
        print("Error: API id '{}' not valid 'load_forecast_api(api_id, station_id)'".format(api_id)) 

def load_visualization(list_forecast_obj, station):
    """
    Load visualization for parameters comparison between APIs for a station.
    
    Parameters:
        list_forecast_obj       list of forecast object to trace data
                                type: `object forecast`
        station                 informations of station
                                type: `dict`
    """
    # get date forecast 
    path_last_img = var.path_last_forecast+"img/{}/{}/".format(station["zone"], station["id"])
    path_archive_img = var.path_archive+"img/{}/{}/".format(station["zone"], station["id"])
    # Trace graphs
    graph_temp = chart.lineChart(list_forecast_obj,"temp")
    graph_precip = chart.lineChart(list_forecast_obj,"precip")
    graph_etp = chart.lineChart(list_forecast_obj,"etp")
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

def load_forecasts(station, visu = True):
    """
    Load and save forecast and visualisation and manage files for a station. 
    Parameters:
        station     station informations
                    type: `dict`
        visu        for creating and saving visualization for APIs comparison as default (set False to ignore this option)
                    type: `Boolean`
    """
    # Get list of api id present in source file
    list_api_id = [api['id'] for api in var.online_api_info]
    # Load forecast for all APIs in source file and keep forecast objects in list for the station 
    list_forecast_obj = []
    for api_id in list_api_id:
        forecast_obj = load_forecast_api(api_id, station)
        list_forecast_obj.append(forecast_obj)
    # Creat and save visualization if not desactivated
    if visu :
        load_visualization(list_forecast_obj, station)

def load_forecasts_all_stations():
    for station in var.stations_info:
        load_forecasts(station)

# =============== main ==============

load_forecasts_all_stations()










