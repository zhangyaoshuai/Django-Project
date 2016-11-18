$(document).ready(function() {
    $.ajax({
        url: '../showIndex/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        success: function(data) {
            var response = data.features;//json data from backend
            var finalResult = data.features;
            var map = L.map('map');
            var markersLayer = new L.LayerGroup();
            var mytiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            });
            map.addLayer(mytiles);
            markersLayer.addTo(map);
            var i = 0;
            showMap(response, i, map, markersLayer);

            //sort by price low to high:
            $("#priceLowToHigh").click(function () {
                sortedData = priceLowToHigh(response);
                var div = $('<div>').attr('id','result-container');
                for (var i=0; i<sortedData.length; i++) {
                    createDiv(div, sortedData, i);
                }
                $("#result-container").replaceWith(div);
            });

            //sort by price high to low:
            $("#priceHighToLow").click(function () {
                sortedData = priceHighToLow(response);
                var div = $('<div>').attr('id','result-container');
                for (var i=0; i<sortedData.length; i++) {
                    createDiv(div, sortedData, i);
                }
                $("#result-container").replaceWith(div);
            });

            //city filter by clicking:
            $("#jersey_city").click(function () {
                response = [];
                var val = "Jersey City";
                var div = $('<div>').attr('id','result-container');
                for(var i=0; i<finalResult.length; i++) {
                    if(finalResult[i].city==val) {
                        response.push(finalResult[i]);
                        createDiv(div, finalResult,i);
                    }
                }
                $("#result-container").replaceWith(div);
                var i =0;
                showMap(response, i, map, markersLayer);
            })

        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });

    $("input:text").focus(
            function () {
                $(this).val('');
            }
        );
});

function showMap(response, i, map, markersLayer) {
    markersLayer.clearLayers();
    var lat = [];
    var lng = [];
    for (i = 0; i < response.length; i++) {
        lat.push(response[i].coordinate[0]);
        lng.push(response[i].coordinate[1]);
    }
    var latMiddle = (Math.max.apply(null, lat) + Math.min.apply(null, lat)) / 2;
    var lngMiddle = (Math.max.apply(null, lng) + Math.min.apply(null, lng)) / 2;
    // Initialise an empty map
    map.setView([latMiddle, lngMiddle], 14);
    for (i = 0; i < response.length; i++) {
        L.marker(response[i].coordinate)
            .bindPopup("<div class='caption'><h4 style='margin-bottom:10px'>$<span class='text-danger'>" +
                response[i].price + "</span></h4></div><a href="+ response[i].id +"><img src=" +
                response[i].picture
                + " style='width:200px; height:150px;' class='img-rounded'/></a><div class='caption'><h4 style='margin:0;'>"
                + response[i].address
                + "</h4><span class='text-primary' style='margin: 0;text-align: left'><h4>"
                + response[i].city + "</h4></span></div>")
            .addTo(map)
            .on('mouseover', function (e) {
                this.openPopup();
            })
            .on('mouseout', function (e) {
                this.closePopup();
            })
            .on('click', function (e) {
                this.off('mouseout');
                this.openPopup();
            })
    }

}

function createDiv(div, sortedData, i) {
    div.append("<div class='thumbnail' style='margin: 0; padding: 0'><a href="+
        sortedData[i].id + "><img class='image-responsive' src=" +
        sortedData[i].picture + " style='height: 250px; width: 100%; margin: 0; padding: 0'></a><div class='caption'><h5 style='margin:0'>" +
        sortedData[i].address + "</h5><span class='text-primary' style='margin: 0;text-align: left'>" +
        sortedData[i].price + "</span><span style='margin: 0;text-align: right'>" +
        sortedData[i].city + "</span><span class='text-danger'>" +
        sortedData[i].bedroom + "bed/" +
        sortedData[i].bathroom + "bath</span></span></div><a href="+
        sortedData[i].id +" class='btn btn-primary btn-sm' role='button'>View Details</a><a href="+
        sortedData[i].id +"/like/" + " class='btn btn-default btn-sm btn-favorite' role='button'><span class='glyphicon glyphicon-star'></span></a><span><small id='favorite_count'>"+
        sortedData[i].favorite_count +"</small></span>")
}
function priceLowToHigh(rentals) {
    rentals.sort(function (a, b) {
        return parseFloat(a.price) - parseFloat(b.price);
    });
    return rentals;
}

function priceHighToLow(rentals) {
    rentals.sort(function (a, b) {
        return parseFloat(b.price) - parseFloat(a.price);
    });
    return rentals;
}
