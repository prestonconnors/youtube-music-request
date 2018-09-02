function initAutocomplete() {
        // Create the autocomplete object, restricting the search to geographical
        // location types.
        autocomplete = new google.maps.places.Autocomplete(
            /** @type {!HTMLInputElement} */(document.getElementById('name')),
            {types: ['geocode', 'establishment']});
};
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
    autocomplete.setBounds(circle.getBounds());
      });
    }
};
