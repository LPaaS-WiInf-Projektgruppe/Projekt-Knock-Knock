

function init() {
   var from_input = document.getElementById('from-input');
   var to_input = document.getElementById('to-input');
   var autocomplete_from = new google.maps.places.SearchBox(from_input);
   var autocomplete_to = new google.maps.places.SearchBox(to_input);
  // var  autocomlete = new google.maps.places.Autocomplete($("#from-input"))
}
google.maps.event.addDomListener(window, 'load', init);

// async function getCoordinates(location)
// {
//   response = await fetch("/geocode_location/" + location);
//   var marker = L.marker([response.json()[0], response.json()[1]]).addTo(map);
//   return response
// }

$("document").ready( () =>
{
  var map = L.map('map').setView([53.599813099076165, 9.932808452732685], 13);
  // var marker = L.marker([53.599813099076165, 9.932808452732685]).addTo(map);
  // var polygon = L.polygon([
  //     [53.599813099076165, 9.932808452732685],
  //     [53.699813099076165, 9.932808452732685]
  // ]).addTo(map);


  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox/dark-v10',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: mapBoxKey
  }).addTo(map);

  var startCoord;
  $('#from-input').focusout( async () =>
  {
    startLocation = $("#from-input").val().trim();
    var response = await fetch("/geocode_location/" + startLocation,  {method:"POST"});
    startCoord = await response.json()
    console.log(startCoord);
    // console.log(response.json());
    var marker = L.marker([startCoord.latitude, startCoord.longitude]).addTo(map);
    map.setView([startCoord.latitude, startCoord.longitude], 13)
  })

  $('#to-input').focusout( async () =>
  {
    console.log("startlocation: " + startCoord);
    var endLocation = $("#to-input").val().trim();
    var response = await fetch("/geocode_location/" + endLocation, {method:"POST"});
    var location = await response.json()
    console.log(location);
    var marker = L.marker([location.latitude, location.longitude]).addTo(map);

    if ($("#to-input").val().strip != "" && $("#from-input").val().strip != "")
    {
      var polygon = L.polygon([
          [startCoord.latitude, startCoord.longitude],
          [location.latitude, location.longitude]
      ]).addTo(map);
    }
  })

  $(".submit-btn").on("click", () =>
  {
    $("#map").css("display", "none");
  })

}
)
