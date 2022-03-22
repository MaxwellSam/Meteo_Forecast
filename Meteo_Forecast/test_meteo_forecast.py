"""
File: test_meteo_forecast.py
Path: 
Description: testing meteo_forecast program
Author: Sam Maxwell
Date: 03/2022
"""

# Imports 

import pandas as pd

## local imports

import modules.variables as var 
import modules.toolbox as tb
import modules.meteo_forecast as forecast

# =============== Localisation infos ==============

# meteoConcept = forecast.MeteoConcept("BrenneBrain")
# openMeteo = forecast.OpenMeteo("BrenneBrain")

# print("\n",meteoConcept.url)
# print(meteoConcept.response.text)
# print(meteoConcept.df_daily)

# print("\n", openMeteo.url)
# print(openMeteo.response.text)
# print(openMeteo.df_daily)
# print(openMeteo.df_hourly)

# save as csv

# path_meteoConcept = var.path_folder_csv + "meteoConcept_forecasts/"
# path_openMeteo = var.path_folder_csv + "openMeteo_forecasts/"

# openMeteo.save(path_openMeteo)
# meteoConcept.save(path_meteoConcept)

# trace graph 

# path_image = var.path_folder_csv + "img/"

# graph_temp = forecast.lineChart([openMeteo, meteoConcept],"temp")
# graph_precip = forecast.lineChart([openMeteo, meteoConcept],"precip")
# graph_etp = forecast.lineChart([openMeteo, meteoConcept],"etp")

# graph_temp.fig.write_image(path_image+"temp.png")
# graph_precip.fig.write_image(path_image+"precip.png")
# graph_etp.fig.write_image(path_image+"etp.png")

# df_etp_hourly = openMeteo.df_hourly[['date', 'etp']]
# print("\ndf_etp_hourly\n", df_etp_hourly)
# df_etp_daily = df_etp_hourly
# # df_etp_daily.date = pd.to_datetime(df_etp_daily.date)
# df_etp_daily = df_etp_daily.resample('D', on='date').sum()
# print("\ndf_etp_daily\n", df_etp_daily)
# df = openMeteo.df_daily.merge(df_etp_daily, on='date')
# print("\nnew df daily\n", df)

# print("\ndaily openMeteo\n", openMeteo.df_daily)

def load_forecasts(station_id):
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










