"""
File: meteo_forecast.py
Path: 
Description: Fetching and data processing on Meteo Forecast
Author: Sam Maxwell
Date: 03/2022
"""

# imports 

from os import sep
import requests
import json
import pandas as pd
from datetime import datetime

import plotly.graph_objects as go 

## local imports

import modules.variables as var


# ================== Forecast Classes ================== #

class forecast:
    def fetch_forecast(self):
        try:
            self.response = requests.get(self.url, verify=False)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    # -------------------- save info -----------------------

    def save_date_forecast(self):
        self.date_init = datetime.now().strftime("%d_%m_%Y_%H")

    # ---------------- Load infos methods ------------------

    def load_api_info(self, api_id):
        for api in var.online_api_info:
            if api["id"] == api_id:
                self.api_info = api
                break
    
    def load_station_info(self, station_id):
        for station in var.stations_info:
            if station["id"] == station_id:
                self.station_info = station
                break
    
    # ------------------ url forecast ----------------------

    def generate_url(self):
        self.url = self.api_info["url_forecast"].replace("LAT", str(self.station_info["coordinates"]['lat'])).replace("LONG", str(self.station_info["coordinates"]['long']))

    # ------------------ trace graph -----------------------

    # def trace(self, fig, param):
    #     if param == "temp":
    #         self.trace_temp(fig)
    #     elif param == "precip":
    #         self.trace_precip(fig)
    #     elif param == "etp":
    #         self.trace_etp(fig)
    
    def trace(self, param):
        if param == "temp":
            return self.trace_temp()
        elif param == "precip":
            return self.trace_precip()
        elif param == "etp":
            return self.trace_etp()


class MeteoConcept(forecast):
    id_api = "meteoConcept"

    def __init__(self, station_id):
        self.save_date_forecast()
        # load info
        self.load_api_info(self.id_api)
        self.load_station_info(station_id)
        # generate url forecast
        self.generate_url()
        # fetch forecast data
        self.fetch_forecast()
        # create dataframes
        self.creat_dataframe()
    
    def creat_dataframe(self):
        json_data = json.loads(self.response.text)
        # select forecast data from json response and convert to dataframe
        df = pd.DataFrame.from_dict(json_data["forecast"])
        # select columns of interest
        self.df_daily = df[self.api_info["parameters"]["daily"].values()]
        # rename columns
        self.df_daily = self.df_daily.rename(columns = dict((v, k) for k, v in self.api_info["parameters"]["daily"].items()))

    def save(self, path):
        path += self.id_api + "_" + self.date_init 
        self.df_daily.to_csv(path+"_daily.csv", sep=';', index=True)

    # ------------------ trace graph -----------------------

    # def trace_temp(self, fig):
    #     fig = fig.add_trace(go.Scatter(
    #         x = self.df_daily["date"],
    #         y = self.df_daily["temp_min"],
    #         name = self.id_api + " temp_min"
    #     ))
    #     fig = fig.add_trace(go.Scatter(
    #         x = self.df_daily["date"],
    #         y = self.df_daily["temp_max"],
    #         name = self.id_api + " temp_max"
    #     ))
    #     return fig

    # def trace_precip(self, fig):
    #     fig.add_trace(go.Scatter(
    #         x = self.df_daily["date"],
    #         y = self.df_daily["precip"],
    #         name = self.id_api + " precip"
    #     ))
    #     return fig
    
    # def trace_etp(self, fig):
    #     fig.add_trace(go.Scatter(
    #         x = self.df_daily["date"],
    #         y = self.df_daily["etp"],
    #         name = self.id_api + " etp"
    #     ))
    #     return fig

    def trace_temp(self):
        dict_1 = {
            "x" : self.df_daily["date"],
            "y" : self.df_daily["temp_min"],
            "name" : self.id_api + " temp_min"
        }
        dict_2 = {
            "x" : self.df_daily["date"],
            "y" : self.df_daily["temp_max"],
            "name" : self.id_api + " temp_max"
        }
        return dict_1, dict_2

    def trace_precip(self):
        dict = {
            "x" : self.df_daily["date"],
            "y" : self.df_daily["precip"],
            "name" : self.id_api + " precip"
        }
        return [dict]

    def trace_etp(self):
        dict = {
            "x" : self.df_daily["date"],
            "y" : self.df_daily["etp"],
            "name" : self.id_api + " etp"
        }
        return [dict]

    

class OpenMeteo(forecast):
    id_api = "openMeteo"

    def __init__(self, station_id):
        self.save_date_forecast()
        # load info
        self.load_api_info(self.id_api)
        self.load_station_info(station_id)
        # generate url forecast
        self.generate_url()
        # fetch forecast data
        self.fetch_forecast()
        # creat dataframes
        self.creat_dataframe()
    
    def creat_dataframe(self):
        json_data = json.loads(self.response.text)
        # select forecast data from json response and convert to dataframe
        self.df_daily = pd.DataFrame.from_dict(json_data["daily"])
        self.df_hourly = pd.DataFrame.from_dict(json_data["hourly"])
        # rename columns 
        self.df_daily = self.df_daily.rename(columns = dict((v, k) for k, v in self.api_info["parameters"]["daily"].items()))
        self.df_hourly = self.df_hourly.rename(columns = dict((v, k) for k, v in self.api_info["parameters"]["hourly"].items()))
    
    def save(self, path):
        path += self.id_api + "_" + self.date_init 
        self.df_daily.to_csv(path+"_daily.csv", sep=';', index=True)
        self.df_hourly.to_csv(path+"_hourly.csv", sep=';', index=True)
    
    # ------------------ trace graph -----------------------

    # def trace_temp(self, fig):
    #     fig = fig.add_trace(go.Scatter(
    #         x = self.df_daily["date"],
    #         y = self.df_daily["temp_min"],
    #         name = self.id_api + " temp_min"
    #     ))
    #     fig = fig.add_trace(go.Scatter(
    #         x = self.df_daily["date"],
    #         y = self.df_daily["temp_max"],
    #         name = self.id_api + " temp_max"
    #     ))
    #     fig = fig.add_trace(go.Scatter(
    #         x = self.df_hourly["date"],
    #         y = self.df_hourly["temp"],
    #         name = self.id_api + " temp (hourly)"
    #     ))
    #     return fig

    # def trace_precip(self, fig):
    #     fig = fig.add_trace(go.Scatter(
    #         x = self.df_daily["date"],
    #         y = self.df_daily["precip"],
    #         name = self.id_api + " precip (daily)"
    #     ))
    #     fig = fig.add_trace(go.Scatter(
    #         x = self.df_hourly["date"],
    #         y = self.df_hourly["precip"],
    #         name = self.id_api + " precip (hourly)"
    #     ))
    #     return fig

    # def trace_etp(self, fig):
    #     fig = fig.add_trace(go.Scatter(
    #         x = self.df_hourly["date"],
    #         y = self.df_hourly["etp"],
    #         name = self.id_api + " etp (hourly)"
    #     ))
    #     return fig

    def trace_temp(self):
        dict_1 = {
            "x":self.df_daily["date"],
            "y":self.df_daily["temp_min"],
            "name":self.id_api + " temp_min"
        }
        dict_2 = {
            "x":self.df_daily["date"],
            "y":self.df_daily["temp_max"],
            "name":self.id_api + " temp_max"
        }
        dict_3 = {
            "x":self.df_hourly["date"],
            "y":self.df_hourly["temp"],
            "name":self.id_api + " temp (hourly)"
        }
        return dict_1, dict_2, dict_3

    def trace_precip(self):
        dict_1 = {
            "x" : self.df_daily["date"],
            "y" : self.df_daily["precip"],
            "name" : self.id_api + " precip (daily)"
        }
        dict_2 = {
            "x" : self.df_hourly["date"],
            "y" : self.df_hourly["precip"],
            "name" : self.id_api + " precip (hourly)"
        }
        return dict_1, dict_2

    def trace_etp(self):
        dict = {
            "x" : self.df_hourly["date"],
            "y" : self.df_hourly["etp"],
            "name" : self.id_api + " etp (hourly)"
        }
        return [dict]
    


# ================== graph Classes ================== #

class lineChart:

    def __init__(self, forecast_obj_list, param):
        self.fig = go.Figure()
        # print(type(self.fig))
        # print(self.fig)
        
        # for obj in forecast_obj_list:
        #     self.fig = obj.trace(self.fig, param)
        list_trace = []
        for obj in forecast_obj_list:
            list_trace.extend(obj.trace(param))

        for trace in list_trace:
            self.fig = self.fig.add_trace(go.Scatter(
                x = trace["x"],
                y = trace["y"],
                name = trace["name"]
            ))



