/**
 * FileName: interface.js
 * Path: ./APP/static/js/interface.js
 * date: 03/2022
 * Description: Interaction with interface.html Page
 */

// ========================== Station ===============================

// ------------------------ local files -----------------------------

fetch('../source_files/stations.json')
.then(response => {
    return response.json()
})
.then(jsondata => console.log(jsondata))

// station_json = require("{url_for('static',filename='/static/source_files/stations.json')}");

// console.log(station_json)

// -------------------------- inputs --------------------------------

var station_selected = document.getElementById("station_selection");
var station = station_selected.options[station_selected.selectedIndex].value //.replaceAll('\'', '\"');

console.log(station)

// test = JSON.parse(station)

// console.log(test)


// -------------------------- outputs --------------------------------

const info_station = document.getElementById("info_station");

info_station.innerHTML = `<b>Latitude:</b> ${station}<br><b>Longitude:</b> ${station}`

// info_station.innerHTML = `<code>${station_selected}</code>`