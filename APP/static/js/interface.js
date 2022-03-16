/**
 * FileName: interface.js
 * Path: ./APP/static/js/interface.js
 * date: 03/2022
 * Description: Interaction with interface.html Page
 */

// ========================== Station ===============================

// ------------------------ local files -----------------------------


// -------------------------- inputs --------------------------------

var station_selection = document.getElementById("station_selection");
var API_selection = document.getElementById("API_selection");
var station = station_selection.options[station_selection.selectedIndex].value
var onlineAPI = API_selection.options[API_selection.selectedIndex].value 

// ------------------------ DataFrames -------------------------------

class Forecast {
    // inputs
    station_selection = document.getElementById("station_selection");
    API_selection = document.getElementById("API_selection");
    // attributes
    station_id;
    api_id;
    url; 
    data;
    // data
    response;

    constructor(){
        this.station_id = station_selection.options[station_selection.selectedIndex].value;
        this.api_id = API_selection.options[API_selection.selectedIndex].value;
        this.url = this.generate_url();
        this.response = this.get_data_forecast();
    }

    generate_url (){
        this.url = window.origin + `/API/${this.station_id}/forecast?station=${this.station_id}`
    } 

    fetch_forecast (){
        this.response = fetch(this.url);
        
    }
}

class Graph{
    params = document.getElementById("params")
}

// -------------------------- outputs --------------------------------

var station_info = document.getElementById("station_info");
var data_API = document.getElementById("data_API");

