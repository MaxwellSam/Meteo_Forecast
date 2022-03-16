"""
File: variables.py
Path: ./modules/variables.py
Description: define variables
Author: Sam Maxwell
Date: 03/2022
"""

## import ##

from distutils.log import error
import json
import requests

## local modules ##

import static.modules.variables as var

# ====================================== API ====================================== #

def get_info_API(onlineAPI, infoType):
    for api in var.online_api_info:
        if api["id"] == onlineAPI:
            return api[infoType]
    return {"Error":404, "info":"method \'get_info_API()\'"}
    

def get_forecast_link(online_api):
    for api in var.online_api_info:
        if api["name"] == online_api:
            return api["url_forecast"]


def generate_url(online_api, station_id):
    url = get_forecast_link(online_api)
    for station in var.stations_info:
        if station["id"] == station_id:
            coordinates = station["coordinates"]
    url = url.replace('LAT', coordinates["lat"])
    url = url.replace('LONG', coordinates["long"])
    return url

def fetch_url(url):
    try: 
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error requests:", e)
        return "error" 
    
def get_forecast(online_api, station_id):
    url = generate_url(online_api, station_id)
    return fetch_url(url)
