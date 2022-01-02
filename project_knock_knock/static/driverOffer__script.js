function init() {
   var from_input = document.getElementById('from-input');
   var to_input = document.getElementById('to-input');
   var autocomplete_from = new google.maps.places.Autocomplete(from_input);
   var autocomplete_to = new google.maps.places.Autocomplete(to_input);
  // var  autocomlete = new google.maps.places.Autocomplete($("#from-input"))
}
google.maps.event.addDomListener(window, 'load', init);
