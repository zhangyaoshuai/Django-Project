 var placeSearch, autocomplete;
      var componentForm = {
      //street_number: 'short_name',
      //route: 'long_name',
      locality: 'long_name',
      //administrative_area_level_1: 'short_name',
      //country: 'long_name',
      postal_code: 'short_name'
    };

      function initAutocomplete() {
        // Create the autocomplete object, restricting the search to geographical
        // location types.
        autocomplete = new google.maps.places.Autocomplete(
            // @type {!HTMLInputElement} 
            (document.getElementById('address')),
            {types: ['geocode']});
        autocomplete.addListener('place_changed', fillInAddress);

      }
      function fillInAddress() {
        // Get the place details from the autocomplete object.
        var place = autocomplete.getPlace();
        //var address = document.getElementById("h_location").value;
        var address = document.getElementById("address").value;
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            //var coordinate = new google.maps.Latlng(latitude, longitude);
            var coordinate = [];
            coordinate.push(latitude);
            coordinate.push(longitude);
            document.getElementById("coordinate").value =  coordinate;
          } else {

            alert('Geocode was not successful for the following reason: ' + status);
            
          }
          });


        // Get each component of the address from the place details
        // and fill the corresponding field on the form.
        for (var i = 0; i < place.address_components.length; i++) {
          var addressType = place.address_components[i].types[0];
          if (componentForm[addressType]) {
            var val = place.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val;
          }
        }
      }
