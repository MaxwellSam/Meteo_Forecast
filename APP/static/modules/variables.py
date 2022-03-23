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

## setup working dir and path to files

wd = os.getcwd() 
path_source_files = "/APP/static/source_files/"

## -------- Sations infos -------- ##
# File path
stations_file_path = wd+path_source_files+"stations.json"
# Load json file
with open(stations_file_path) as json_file: 
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





