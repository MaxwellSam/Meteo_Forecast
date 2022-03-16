"""
File: APP.py
Path: ./API/API.py
Description: APP for Meteo Forecast
Author: Sam Maxwell
Date: 03/2022
"""

## Import ##

from flask import Flask, request, render_template, url_for
import json

## Local modules ##

import static.modules.variables as var
import static.modules.toolbox as tb

## classes ##

# ------------------------------- Initialization ----------------------------- #

APP = Flask(__name__)

# ------------------------------------ Home ---------------------------------- #

@APP.route("/")
def home():
    return render_template("interface.html", stations=var.stations_info, online_api=var.online_api_info)

# ------------------------------------- API ---------------------------------- #

@APP.route("/API")
def api():
    return render_template("api.html")

@APP.route("/API/<onlineAPI>/info/<infoType>")
def infoAPI(onlineAPI, infoType):
    return tb.get_info_API(onlineAPI, infoType)

@APP.route("/API/<online_api>/forecast")
def forecast(online_api):
    return tb.get_forecast(online_api, request.args.get("station"))

@APP.route("/API/<online_api>/forecast/link")
def forecast_link(online_api):
    return tb.get_forecast_link(online_api)


# ---------------------------------- Run APP --------------------------------- #

if __name__ == "__main__":
    APP.run(debug=True)