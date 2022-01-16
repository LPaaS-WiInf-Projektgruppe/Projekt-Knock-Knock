// var config = require('config.json')
// import mapBoxkey from "config.json"

// var mapBoxKey = config.map_box_key

$("document").ready( () =>
{


  var map = L.map('map', {preferCanvas: true}).setView([53.599813099076165, 9.932808452732685], 13);
  // var marker = L.marker([53.599813099076165, 9.932808452732685]).addTo(map);


  // https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/dark-v10',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: mapBoxKey
    }).addTo(map);



  async function get_coordinates(name)
  {
    response = await fetch("/com_offer_coordinates", {method: "POST"})
    coordinates = await response.json()

  return await coordinates;
}

(async () => {

  coordinates = await get_coordinates()

  for (i = 0; i < coordinates.length;  i++)
  {
  // var marker = L.marker(coordinates[i][1]).addTo(map);

  if (i == 0 | i == 1 | i == 2 | i == 3 | i == 4 | i == 24)
  {
    var polygon = L.polygon([
        coordinates[i][1],
        coordinates[i][2]
    ]).addTo(map);
  }

  if (i != 24)
  {
    var marker =  L.circle(coordinates[i][1], 100, {color:"green"}).addTo(map);
    var marker =  L.circle(coordinates[i][2], 100, {color:"red"}).addTo(map);
    var polygon = L.polygon([
        coordinates[i][1],
        coordinates[i][2]
    ]).addTo(map);
  }
  else
  {
    var marker =  L.circle(coordinates[i][1], 200, {color:"yellow"}).addTo(map);
  }
}



})()


})
