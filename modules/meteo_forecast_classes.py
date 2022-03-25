"""
File: meteo_forecast_classes.py
Path: ./modules/meteo_forecast_classes.py
Description: Fetching and data processing on Meteo Forecast
Author: Sam Maxwell
Date: 03/2022
"""

# imports 

import os 
import json
import pandas as pd
from datetime import datetime
import numpy as np

## local imports

import modules.variables as var
import modules.toolbox as tb


# ================== Forecast Classes ================== #

class Forecast:
    """
    Parent Class for Meteo Forecast data

    Attributes:
        date_init           Class initialisation date (or date of forecast), format 'Y_m_d_H'
                            type: `string`
        api_info            API informations (id, name, link, url base, parameters) from source file 'source_files/online_api.json'
                            type: `dict`
        station_info        station informations (id, name, zone, localisation) from source file 'source_files/station.json'
                            type: `dict`
        url                 URL for API request with the station coordinates (longitude and latitude)
                            type: `string` 
        response            response of API call 
                            type `response object`
        dataframes          forecast Dataframes (forecast type as key, and dataframe as value)
                            type: dict<`string`, `pandas Dataframe object`>
    Methods:
        fetch_forecast()                    Request API with URL generated and save response as attribute.  
        save_date_forecast()                Save initialization date corresponding to the meteo forecast date.
        load_api_info(api_id)               Get and add station info from source file as attribute.
        load_station_info(station_id)       Get and add API info from source file as attribute.
        generate_url()                      Generate and add URL for API call as attribute.
        __create_dataframe()                Generate daily and hourly forecast dataframes. 
        save(path)                          Save dataframe as csv.
        trace()                             Generate and return trace for visualization. 
        

    """ 

    def __init__(self):
        """
        Class initialisation
        """
        # save curent date
        self.save_date_forecast()
        # create dataframes
        self.__create_dataframe()


    def fetch_forecast(self):
        """
        Request API with URL generated and save response as attribute. 
        """
        self.response = tb.fetch_url(self.url)
    

    # -------------------- save info -----------------------

    def save_date_forecast(self):
        """
        Save initialization date corresponding to the meteo forecast date.
        """
        self.date_init = datetime.now().strftime("%Y_%m_%d_%H")

    # ---------------- Load infos methods ------------------

    def load_api_info(self, api_id):
        """
        Get and add station info from source file as attribute.

        Parameters:
            api_id      API ID in json source file (./Meteo_Forecast/source_files/online_api.json) 
                        type: `string`
        """
        for api in var.online_api_info:
            if api["id"] == api_id:
                self.api_info = api
                break
    
    def load_station_info(self, station_id):
        """
        Get and add API info from source file as attribute.
        
        Parameters:
            station_id      id station in json source file (./Meteo_Forecast/source_files/stations_json) 
                            type: `string`
        """
        for station in var.stations_info:
            if station["id"] == station_id:
                self.station_info = station
                break
    
    # ------------------ url forecast ----------------------

    def generate_url(self):
        """
        Generate and add URL for API call as attribute.
        """
        self.url = self.api_info["url_forecast"].replace("LAT", str(self.station_info["coordinates"]['lat'])).replace("LONG", str(self.station_info["coordinates"]['long']))

    # ---------------- Dataframe ------------------

    def __create_dataframe(self):
        """
        Create pandas dataframes with forecast data extracted from response.
        """
        self.dataframes = {}
        # select info forecast availables
        forecasts_availables = {k:v for k, v in self.api_info['parameters'].items() if v != None}
        for forecast_type, parameters in forecasts_availables.items():
            # Separete parameters available to parameters not available in the forecast data
            parameters_availables = {k:v for k,v in parameters.items() if v != None}
            parameters_not_availables = {k:v for k,v in parameters.items() if v == None}
            # creat the dataframe for available parameters
            df = pd.DataFrame(self.data[forecast_type])
            df = df[parameters_availables.values()]
            # rename columns
            df = df.rename(columns={v:k for k, v in parameters_availables.items()})
            # add columns not availables with NaN value
            for param in parameters_not_availables.keys():
                df[param] = np.NaN
            # converte date to dateTime
            df.date = pd.to_datetime(df.date)
            # add forecast dataframe to dataframes 
            self.dataframes[forecast_type] = df
    
    def save(self, path):
        """
        Save dataframes in csv format at the specific path as "{API_ID}_{DATE}_{FORECAST TYPE}.csv"

        Parameters:
            path        file path to save dataframes csv
                        type: `string`
        """
        for forecast_type, df in self.dataframes.items():
            # change date format
            df.date = df.date.map(lambda d : d.strftime('%Y-%m-%d %H:%M'))
            #  create file name
            file_name = "{}_{}_{}_{}.csv".format(self.id_api, self.station_info['id'], self.date_init, forecast_type)
            # save file 
            print("# Save file '{}' ... ".format(file_name), end="") 
            self.dataframes[forecast_type].to_csv(os.path.normpath(path+file_name), sep=',', na_rep="\\N", columns=var.config_info["data"]["columns"]["order"][forecast_type], index=False)
            print("Done")




    
    # ------------------ trace graph -----------------------
    
    def trace(self, param):
        """
        Generate and return trace for parameters visualization (temp, precip or etp)
        Return:
            self.trace_temp()
            or                          Traces for the specific parameters.    
            self.trace_precip()         type: `dict`
            or
            self.trace_etp()
        """
        if param == "temp":
            return self.trace_temp()
        elif param == "precip":
            return self.trace_precip()
        elif param == "etp":
            return self.trace_etp()


class MeteoConcept(Forecast):
    """
    Class for MeteoConcept API forecast.

    Child class of `Forecast` parent class. adapted to the structure 
    of MeteoConcept API response to formate and save forecast data. 

    Initialisation parameters:
        station_id      Station ID to get forecast
                        type: `string`

    Attributs:
        dataframes['daily']        Daily forecast Dataframe
                        type: `pandas Dataframe object`
    
    Methods: 
        __create_dataframe()        Generate daily forecast dataframe. 
        save(path)                  Save dataframe as csv.
        trace_temp()                Generate traces for visualization of temperature parameter
        trace_precip()              Generate traces for visualization of precipitation parameter
        trace_etp()                 Generate trace for visualization of evapotranspiration parameter     
    """
    id_api = "meteoConcept"

    def __init__(self, station_id):
        """
        Class initialization
        """
        # # save curent date
        # self.save_date_forecast()
        # load info
        self.load_api_info(self.id_api)
        self.load_station_info(station_id)
        # generate url forecast
        self.generate_url()
        # fetch forecast data
        self.fetch_forecast()
        # prepare data 
        json_data = json.loads(self.response.text)
        self.data = {'daily': json_data['forecast']}
        # # create dataframes
        # self.create_dataframe()
        Forecast.__init__(self)
        self.__complete_dataframes()


    
    # ------------------ dataframe -----------------------

    def __complete_dataframes(self):
        """
        Creat daily forecast dataframe. 
        """
        # replace negative etp to NaN value
        for df in self.dataframes.values():
            df[df['etp'] < 0] = np.NaN

    # ------------------ trace graph -----------------------

    def trace_temp(self):
        """
        Format temperature data for graph trace.  
        """
        # Prepare traces
        dict_1 = {
            "x" : self.dataframes['daily']["date"],
            "y" : self.dataframes['daily']["temp_min"],
            "name" : self.id_api + " temp_min"
        }
        dict_2 = {
            "x" : self.dataframes['daily']["date"],
            "y" : self.dataframes['daily']["temp_max"],
            "name" : self.id_api + " temp_max"
        }
        return dict_1, dict_2

    def trace_precip(self):
        """
        Format precipitation data for graph trace.  
        """
        # Prepare trace
        dict = {
            "x" : self.dataframes['daily']["date"],
            "y" : self.dataframes['daily']["precip"],
            "name" : self.id_api + " precip"
        }
        return [dict]

    def trace_etp(self):
        """
        Format etp data for graph trace.  
        """
        df_d = self.dataframes['daily'].dropna(subset=['etp']) # .drop(self.dataframes['daily'].index[self.dataframes['daily']["etp"] < 0].tolist(), inplace=True)
        # print("\n  meteoConcept\n", self.dataframes['daily'], "\n")
        # Prepare tace
        dict = {
            "x" : df_d["date"],
            "y" : df_d["etp"],
            "name" : self.id_api + " etp"
        }
        return [dict]

    

class OpenMeteo(Forecast):
    """
    Class for OpenMeteo API forecast.
    
    Child class of `Forecast` parent class. adapted to the structure 
    of OpenMeteo API response to formate and save forecast data. 

    Initialisation parameters:
        station_id      Station ID to get forecast
                        type: `string`

    Attributs:
        data            data formated for dataframe creation (forecast type as key, and data as value) 
                        type: dict
    
    Methods: 
        trace_temp()                Generate traces for visualization of temperature parameter
        trace_precip()              Generate traces for visualization of precipitation parameter
        trace_etp()                 Generate trace for visualization of evapotranspiration parameter  
    """
    id_api = "openMeteo"

    def __init__(self, station_id):
        """
        Class initialization
        """
        # # save curent date
        # self.save_date_forecast()
        # load info
        self.load_api_info(self.id_api)
        self.load_station_info(station_id)
        # generate url forecast
        self.generate_url()
        # fetch forecast data
        self.fetch_forecast()
        # prepare data 
        json_data = json.loads(self.response.text)
        self.data = {
            'daily':json_data['daily'],
            'hourly':json_data['hourly'] 
            }
        # # create dataframes
        # self.create_dataframe()
        Forecast.__init__(self)
        self.__complete_dataframes()
    
    def __complete_dataframes(self):
        """
        Creat daily forecast dataframe. 
        """
        # Calcul daily etp
        df_etp = self.dataframes['hourly'][['etp', 'date']]
        df_etp = df_etp.resample('D', on='date').sum()
        self.dataframes['daily'].etp = df_etp.etp.values
    
    # ------------------ trace graph -----------------------

    def trace_temp(self):
        """
        Format temperature data for graph trace.  
        """
        # Prepare traces 
        dict_1 = {
            "x":self.dataframes['daily']["date"],
            "y":self.dataframes['daily']["temp_min"],
            "name":self.id_api + " temp_min"
        }
        dict_2 = {
            "x":self.dataframes['daily']["date"],
            "y":self.dataframes['daily']["temp_max"],
            "name":self.id_api + " temp_max"
        }
        dict_3 = {
            "x":self.dataframes['hourly']["date"],
            "y":self.dataframes['hourly']["temp"],
            "name":self.id_api + " temp (hourly)"
        }
        return dict_1, dict_2, dict_3

    def trace_precip(self):
        """
        Format precipitation data for graph trace.  
        """
        # Prepare traces
        dict_1 = {
            "x" : self.dataframes['daily']["date"],
            "y" : self.dataframes['daily']["precip"],
            "name" : self.id_api + " precip (daily)"
        }
        dict_2 = {
            "x" : self.dataframes['hourly']["date"],
            "y" : self.dataframes['hourly']["precip"],
            "name" : self.id_api + " precip (hourly)"
        }
        return dict_1, dict_2

    def trace_etp(self):
        """
        Format etp data for graph trace.  
        """
        df_d = self.dataframes['daily'].dropna(subset=['etp']) # drop(self.dataframes['daily'][self.dataframes['daily']['etp'] < 0].index, inplace=True)
        # print("\n  openMeteo (daily)\n", self.dataframes['daily'], "\n")
        # print("\n  openMeteo (hourly)\n", self.dataframes['hourly'], "\n")
        df_h = self.dataframes['hourly'].dropna(subset=['etp']) #drop(self.dataframes['hourly'][self.dataframes['hourly']['etp'] < 0].index, inplace=True)
        # Prepare traces 
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
    
