

$("document").ready( () =>
{

  // response = await fetch("/com_offer_coordinates", {method: "POST"})
  // coordinates = await response.json()

  //
  // for (coordinate in coodinates)
  // {
  //   var marker = L.marker([coordinates[2][0], coordinates[2][1]]).addTo(map);
  //   var marker = L.marker([coordinates[2][0], coordinates[2][1]]).addTo(map);
  // }

  var map = L.map('map', {preferCanvas: true}).setView([53.599813099076165, 9.932808452732685], 13);
  // var marker = L.marker([53.599813099076165, 9.932808452732685]).addTo(map);


  // https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/dark-v10',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1Ijoiam9leTE1MTciLCJhIjoiY2t5MXJwODFyMDIzczJubjExbm90aHc3YSJ9.8Ildv_V7RY38fLBWWxmt2Q'
    }).addTo(map);

  // var polygon = L.polygon([
  //     [53.599813099076165, 9.932808452732685],
  //     [53.699813099076165, 9.932808452732685]
  // ]).addTo(map);
  //
  //
  //
  //
  //
  // var polygon = L.polygon([
  //     [53.599813099076165, 9.932808452732685],
  //     [53.599813099076165, 9.942808452732685]
  // ]).addTo(map);

  async function get_coordinates(name)
  {
    response = await fetch("/com_offer_coordinates", {method: "POST"})
    coordinates = await response.json()
    for (i = 0; i < coordinates.length;  i++)
    {
    var marker = L.marker(coordinates[i][1]).addTo(map);
    var marker = L.marker(coordinates[i][2]).addTo(map);
  }
  // return await coordinates;
}

// (async () => {
	// console.log(await get_coordinates())
  // coordinates = await get_coordinates()
  // console.log(coordinates.length);
  // for (i = 0; i < coordinates.length;  i++)
  // {
  //   // console.log(coordinates[i][1]);
  //
  //   // if (i == 1)
  //   // {
  //   //   var marker = L.circle(coordinates[i][1], 500, {fillColor:"green"}).addTo(map);
  //   //
  //   //   var marker =  L.circle(coordinates[i][2], 500, {fillColor:"green"}).addTo(map);
  //   //
  //   //
  //   //
  //   // }
  //   // else
  //   // {
  //   //   var marker = L.marker(coordinates[i][1]).addTo(map);
  //   //   var marker = L.marker(coordinates[i][2]).addTo(map);
  //   // }
  //
  //
  //
  //     if ((i < coordinates.length - 1) && (i >= 0))
  //     {
  //       console.log("entered if case");
  //       var polygon = L.polygon([
  //           coordinates[i][1],
  //           coordinates[i + 1][1]
  //       ]).addTo(map);
  //     }
  // }


//
// })()





})
function openTab(name)
{
  var i;
  var x = document.getElementsByClassName("profile");
  var tabs = document.getElementsByClassName("tab");
  for (var i = 0; i < x.length; i++)
  {
    x[i].style.display = "none";
    tabs[i].style.background = "#7E888A";
  }
  document.getElementById(name).style.display = "block";
  document.getElementById(name + "-tab").style.backgroundColor = "white";
}
