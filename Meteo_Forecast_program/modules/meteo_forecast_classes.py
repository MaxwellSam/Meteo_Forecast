"""
File: meteo_forecast.py
Path: 
Description: Fetching and data processing on Meteo Forecast
Author: Sam Maxwell
Date: 03/2022
"""

# imports 

from cmath import nan
from operator import index
import os 
import json
import pandas as pd
from datetime import datetime
import numpy as np

import plotly.graph_objects as go
from pyparsing import col 

## local imports

import modules.variables as var
import modules.toolbox as tb


# ================== Forecast Classes ================== #

class forecast:
    def fetch_forecast(self):
        """
        Request API and get response. 
        """
    #     try:
    #         self.response = requests.get(self.url, verify=False)
    #     except requests.exceptions.RequestException as e:
    #         raise SystemExit(e)
        self.response = tb.fetch_url(self.url)
    

    # -------------------- save info -----------------------

    def save_date_forecast(self):
        self.date_init = datetime.now().strftime("%Y_%m_%d_%H")

    # ---------------- Load infos methods ------------------

    def load_api_info(self, api_id):
        """
        Load info API

        Param:
            api_id : id api in json source file (./Meteo_Forecast/source_files/online_api.json) 
        """
        for api in var.online_api_info:
            if api["id"] == api_id:
                self.api_info = api
                break
    
    def load_station_info(self, station_id):
        """
        Load info station

        Param:
            station_id : id station in json source file (./Meteo_Forecast/source_files/stations_json) 
        """
        for station in var.stations_info:
            if station["id"] == station_id:
                self.station_info = station
                break
    
    # ------------------ url forecast ----------------------

    def generate_url(self):
        """
        Generate url for requesting the meteo API 
        """
        self.url = self.api_info["url_forecast"].replace("LAT", str(self.station_info["coordinates"]['lat'])).replace("LONG", str(self.station_info["coordinates"]['long']))

    # ------------------ trace graph -----------------------
    
    def trace(self, param):
        """
        Creat trace for graph according to param (temp, precip or etp)
        """
        if param == "temp":
            return self.trace_temp()
        elif param == "precip":
            return self.trace_precip()
        elif param == "etp":
            return self.trace_etp()


class MeteoConcept(forecast):
    """
    Class for MeteoConcept API forecast.
    Description: 
        This class request the API Meteoconcept online and load meteoforecast as pandas Dataframe. 
        This one could be save as csv and trace created for visualisation. 
    """
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
    
    # ------------------ dataframe -----------------------

    def creat_dataframe(self):
        """
        Creat daily forecast dataframe. 
        """
        json_data = json.loads(self.response.text)
        # select forecast data from json response and convert to dataframe
        df = pd.DataFrame.from_dict(json_data["forecast"])
        # select columns of interest
        self.df_daily = df[self.api_info["parameters"]["daily"].values()]
        # rename columns
        self.df_daily = self.df_daily.rename(columns = dict((v, k) for k, v in self.api_info["parameters"]["daily"].items()))
        # converte date to dateTime
        self.df_daily.date = pd.to_datetime(self.df_daily.date)
        # replace negative etp value by NaN value
        self.df_daily[self.df_daily['etp'] < 0] = np.NaN

    # ----------------- save dataframe -----------------------

    def save(self, path):
        """
        Save dataframe in csv format at the specific path as "meteoConcept_{DATE}_{FORECAST TYPE}.csv"
        """
        # modify date time format
        # print("\n",self.df_daily.dtypes, "\n")
        self.df_daily.date = self.df_daily.date.map(lambda d : d.strftime('%Y-%m-%d %H:%M'))
        # print(self.df_daily.date)
        # generate file name
        f_daily = "{}_{}_{}_daily.csv".format(self.id_api, self.station_info['id'], self.date_init)
        # save file 
        print("# Save file '{}' ... ".format(f_daily), end="") 
        self.df_daily.to_csv(os.path.normpath(path+f_daily), sep=',', na_rep="\\N", columns=['date','temp_min', 'temp_max', 'etp', 'precip', 'proba_precip'], index=False)
        print("Done")

    # ------------------ trace graph -----------------------

    def trace_temp(self):
        """
        Format temperature data for graph trace.  
        """
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
        """
        Format precipitation data for graph trace.  
        """
        dict = {
            "x" : self.df_daily["date"],
            "y" : self.df_daily["precip"],
            "name" : self.id_api + " precip"
        }
        return [dict]

    def trace_etp(self):
        """
        Format etp data for graph trace.  
        """
        # df_d = self.df_daily.drop(self.df_daily[self.df_daily["etp"] < 0].index, inplace=True)
        df_d = self.df_daily.dropna(subset=['etp']) # .drop(self.df_daily.index[self.df_daily["etp"] < 0].tolist(), inplace=True)
        print("\n  meteoConcept\n", self.df_daily, "\n")
        # print("\n meteoConcept\n", self.df_daily.index[self.df_daily["etp"] < 0].tolist(), "\n")
        # print("\n", df_d, "\n")
        # dict = {
        #     "x" : self.df_daily["date"],
        #     "y" : self.df_daily["etp"],
        #     "name" : self.id_api + " etp"
        # }
        dict = {
            "x" : df_d["date"],
            "y" : df_d["etp"],
            "name" : self.id_api + " etp"
        }
        return [dict]

    

class OpenMeteo(forecast):
    """
    Class for OpenMeteo API forecast.
    Description: 
        This class request the API OpenMeteo online and load meteo forecast as pandas Dataframe. 
        This one could be save as csv and trace created for visualisation. 
    """
    id_api = "openMeteo"

    def __init__(self, station_id):
        # save initialization date 
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
    
    def add_daily_etp(self):
        """
        Calcul and add etp to daily data
        """
        # extract etp from hourly data
        df_etp_hourly = self.df_hourly[['etp', 'date']]
        # sum etp values for same days to create daily forecast
        df_etp_daily = df_etp_hourly.resample('D', on='date').sum()
        # add daily etp to daily dataframe
        self.df_daily = self.df_daily.merge(df_etp_daily, on='date')
    
    def creat_dataframe(self):
        """
        Creat hourly and daily forecasts dataframes. 
        """
        json_data = json.loads(self.response.text)
        # select forecast data from json response and convert to dataframe
        self.df_daily = pd.DataFrame.from_dict(json_data["daily"])
        self.df_hourly = pd.DataFrame.from_dict(json_data["hourly"])
        # rename columns 
        self.df_daily = self.df_daily.rename(columns = dict((v, k) for k, v in self.api_info["parameters"]["daily"].items()))
        self.df_hourly = self.df_hourly.rename(columns = dict((v, k) for k, v in self.api_info["parameters"]["hourly"].items()))
        # converte date to dateTime
        self.df_daily.date = pd.to_datetime(self.df_daily.date)
        self.df_hourly.date = pd.to_datetime(self.df_hourly.date)
        # add etp daily
        self.add_daily_etp()
        # add proba_precip columns with NaN value
        self.df_daily["proba_precip"] = np.NaN
        # replace negative etp value by NaN value
        self.df_daily[self.df_daily['etp'] < 0] = np.NaN
        self.df_hourly[self.df_hourly['etp'] < 0] = np.NaN
    
    def save(self, path):
        """
        Save dataframes in csv format at the specific path as "OpenMeteo_{DATE}_{FORECAST TYPE}.csv"
        """
        # change date format
        # self.df_daily.date = self.df_daily.date.dt.strftime('%d-%m-%Y %H:%M')
        # self.df_hourly.date = self.df_hourly.date.dt.strftime('%d-%m-%Y %H:%M')
        self.df_daily.date = self.df_daily.date.map(lambda d : d.strftime('%d-%m-%Y %H:%M'))
        self.df_hourly.date = self.df_hourly.date.map(lambda d : d.strftime('%d-%m-%Y %H:%M'))
        # generate files name
        f_daily = "{}_{}_{}_daily.csv".format(self.id_api, self.station_info['id'], self.date_init)
        f_hourly = "{}_{}_{}_hourly.csv".format(self.id_api, self.station_info['id'], self.date_init)
        # save files
        ## daily
        print("# Save file '{}' ... ".format(f_daily), end="") 
        self.df_daily.to_csv(os.path.normpath(path+f_daily), sep=',', na_rep="\\N", columns=['date','temp_min', 'temp_max', 'etp', 'precip', 'proba_precip'], index=False)
        print("Done")
        ## daily
        print("# Save file '{}' ... ".format(f_hourly), end="") 
        self.df_hourly.to_csv(os.path.normpath(path+f_hourly), sep=',', na_rep="\\N", columns=['date','temp', 'etp', 'precip'], index=False)
        print("Done")
    
    # ------------------ trace graph -----------------------

    def trace_temp(self):
        """
        Format temperature data for graph trace.  
        """
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
        """
        Format precipitation data for graph trace.  
        """
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
        """
        Format etp data for graph trace.  
        """
        df_d = self.df_daily.dropna(subset=['etp']) # drop(self.df_daily[self.df_daily['etp'] < 0].index, inplace=True)
        print("\n  openMeteo (daily)\n", self.df_daily, "\n")
        print("\n  openMeteo (hourly)\n", self.df_hourly, "\n")
        # print("\n openMeteo\n", self.df_daily[self.df_daily['etp'] < 0].index, "\n")
        # print("\n", df_d, "\n")
        df_h = self.df_hourly.dropna(subset=['etp']) #drop(self.df_hourly[self.df_hourly['etp'] < 0].index, inplace=True)
        # dict_1 = {
        #     "x" : self.df_hourly["date"],
        #     "y" : self.df_hourly["etp"],
        #     "name" : self.id_api + " etp (hourly)"
        # }
        # dict_2 = {
        #     "x" : self.df_daily["date"],
        #     "y" : self.df_daily["etp"],
        #     "name" : self.id_api + " etp (daily)"
        # }
        dict_1 = {
            "x" : df_h["date"],
            "y" : df_h["etp"],
            "name" : self.id_api + " etp (hourly)"
        }
        dict_2 = {
            "x" : df_d["date"],
            "y" : df_d["etp"],
            "name" : self.id_api + " etp (daily)"
        }
        return dict_1, dict_2
    


# ================== graph Classes ================== #

class lineChart:

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
        # print(type(self.fig))
        # print(self.fig)
        
        # for obj in forecast_obj_list:
        #     self.fig = obj.trace(self.fig, param)

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




