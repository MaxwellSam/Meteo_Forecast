"""
File: variables.py
Path: ./modules/variables.py
Description: define variables
Author: Sam Maxwell
Date: 03/2022
"""

## import ##

import json
import os  

# ====================================== API ====================================== #

## Sations infos ##

wd = os.getcwd()
path_source_files = "/APP/static/source_files/"
stations_path = wd+path_source_files+"stations.json"

with open(stations_path) as json_file: 
    stations_json = json.load(json_file)

stations = stations_json["stations"]

## URL API online ##

url_API_meteo_concept = "https://api.meteo-concept.com/api/forecast/daily?"
token_meteo_concept = "1e2e5883e15615e81b09e24a0f2d5ed0f39acc7af3bb6c5687c3975fed43bd82"


