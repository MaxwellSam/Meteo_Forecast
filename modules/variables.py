"""
File: variables.py
Path: 
Description: variables for Meteo Forecast program
Author: Sam Maxwell
Date: 03/2022
"""
## import ##

import json
import os  

# ===================== Load source Files ===================== # 

## setup working dir and path to files

# wd = os.getcwd().split("Meteo_Forecast")[0]
wd = os.getcwd() #.path.abspath(os.getcwd()) # os.getcwd()
path_source_files = "/source_files/" # Enter path to source file directory from curent dir where python program is exectuted

## -------- Sations infos -------- ##

# File path
stations_file_path = wd+path_source_files+"stations.json"
# Load json file
with open(os.path.normpath(stations_file_path)) as json_file: 
    stations_json = json.load(json_file)
# get stations list from dict
stations_info = stations_json["stations"]

## ------ Online API infos ------- ##

# File path
api_file_path = wd+path_source_files+"online_api.json"
# Load json file
with open(api_file_path) as json_file:
    online_api_json = json.load(json_file)
# get API list from dict 
online_api_info = online_api_json["API"]

## ----------- config ------------- ##

# File path 
config_file_path = wd+path_source_files+"config.json"
# Load json file
with open(config_file_path) as json_file:
    config_info = json.load(json_file)

# ===================== Save forecast data ===================== #

# path_folder_csv = wd+"/Meteo_Forecast/Meteo_Forecast_program/forecast_data/"
path_folder_csv = wd+"/forecast_data/"
# last forecast directory
path_last_forecast = path_folder_csv+"last_forecasts/"
# archive directory
path_archive = path_folder_csv+"archive/"
# images directory
path_images = path_folder_csv+"img/"