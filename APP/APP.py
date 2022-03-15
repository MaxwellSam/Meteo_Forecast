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

import modules.variables as var

## classes ##

# ------------------------------- Initialization ----------------------------- #

APP = Flask(__name__)

# ------------------------------------ Home ---------------------------------- #

@APP.route("/")
def home():
    return render_template("interface.html", stations=var.stations)

# ------------------------------------- API ---------------------------------- #

@APP.route("/API")
def api():
    return render_template("api.html")

# ---------------------------------- Run APP --------------------------------- #

if __name__ == "__main__":
    # APP.run(host='0.0.0.0', port=5000, debug=True)
    APP.run(debug=True)