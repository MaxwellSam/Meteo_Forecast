# Meteo Forecast

## Description

Research project in order to develope automatic meteo forecast data recovery for water flow prediction model. 

The purpose was to find meteorological forecasts in open data online for automatic recovery for temperature, precipitation and evapotransiration.  

## Project architecture

```
.
|
| _ forecast_data
|   | _ archive 
|   | _ last_forecasts
|
| _ modules
|   | _ meteo_forecast_classes.py
|   | _ toolbox.py
|   | _ variables.py
|
| _ source_files 
|   | _ online_api.json
|   | _ stations.json
|
| _ meteo_forecast.py

```

## Meteo_Forecast program 

Program to save and archive  meteo forecasts data from online APIs. This program request the following APIs:
- [OpenMeteo](https://open-meteo.com/en), forecast in open data for 7 days.  
- [MeteoConcept](https://api.meteo-concept.com/), forecast free for 14 days. 

Weather parameters needed for the project and saved from API response are temperature, precipitation, and evapotranspiration. 

### Python dependancies

`Python3` version was used to develope the program. 
The following packages need to be installed before running the program:
- for API calls and data manipulation
  - `requests`
  - `pandas`
- for files managment
  - `os`
- for visualisation
  - `plotly` 
  - `kaleido` 

### Run the program 

Be sure to be located at the project root `/Meteo_Forecast/.` and run the command line `python3 meteo_forecast.py`





