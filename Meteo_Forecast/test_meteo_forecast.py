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

meteoConcept = forecast.MeteoConcept("BrenneBrain")
openMeteo = forecast.OpenMeteo("BrenneBrain")

print("\n",meteoConcept.url)
# print(meteoConcept.response.text)
print(meteoConcept.df_daily)

print("\n", openMeteo.url)
# print(openMeteo.response.text)
print(openMeteo.df_daily)
print(openMeteo.df_hourly)

# save as csv

path_meteoConcept = var.path_folder_csv + "meteoConcept_forecasts/"
path_openMeteo = var.path_folder_csv + "openMeteo_forecasts/"

openMeteo.save(path_openMeteo)
meteoConcept.save(path_meteoConcept)

# trace graph 

path_image = var.path_folder_csv + "img/"

graph_temp = forecast.lineChart([openMeteo, meteoConcept],"temp")
graph_precip = forecast.lineChart([openMeteo, meteoConcept],"precip")
graph_etp = forecast.lineChart([openMeteo, meteoConcept],"etp")

graph_temp.fig.write_image(path_image+"temp.png")
graph_precip.fig.write_image(path_image+"precip.png")
graph_etp.fig.write_image(path_image+"etp.png")














