
$(document).ready(function() {
    //global variable:
    var dump = [];
    var response = [];
    /*
    //initialize map:
    var map = L.map('map');
    var mytiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });
    map.addLayer(mytiles);
    var markers = new L.LayerGroup().addTo(map);
    */
    //asyncronously getting backend json data from url: /getRentals/
    $.ajax({
        url: '../getRentals/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        success: function(data) {
            //on success to pass data to global variable
            response = data;
            dump = response;
            //showMap(response, markers, map);

        },
        failure: function(data) {
            alert('Got an error!');
        }
    });
    //sort by price low to high:
    $("#priceLowToHigh").click(function () {
        //sort
        sortedData = priceLowToHigh(response);
        //replace html element with new sorted element
        createDiv(sortedData);
        //update map
        showMap(response, markers, map);
    });

    //sort by price high to low:
    $("#priceHighToLow").click(function () {
        sortedData = priceHighToLow(response);
        createDiv(sortedData);
        showMap(response, markers, map);
    });
    //sort by time created:
    $("#newest").click(function () {
        sortedData = newest(response);
        createDiv(sortedData);
        showMap(response, markers, map);
    });

    //filter by price:
    $("#searchPrice").click(function () {
        response = dump;
        var min_price = $("#min_price").val();
        var max_price = $("#max_price").val();
        if(min_price == '') {
            min_price = 0;
        }
        if(max_price == '') {
            max_price = 5000;
        }
        var result = [];
        for (var i=0; i<response.length; i++) {
            if(response[i].price>=min_price && response[i].price<=max_price) {
                result.push(response[i]);
            }
        }
        //dynamically update html element
        createDiv(result);
        showMap(result, markers, map);
        //pass filterd value to global variable
        response = result;
    });

    //search by key word:
    $('#searchForm').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '../getRentals/',
            data: {
                query: $('#query').val()
            },

            //csrf_token
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),

            success: function (data) {
                var result = data;
                //pass result to global variable
                response = result;
                dump = response;
                //update map
                showMap(result, markers, map);
                if (result.length>0) {
                    createDiv(result)
                }

                //for empty result
                else {
                    var div = $('<div>').attr({'class': 'col-sm-3 col-md-3',
                                    'id': 'result-container'});
                    div.append("<div class='row'><div class='alert alert-warning' style='margin: 0;'><p style='text-align: center'><strong>No results</strong></p></div></div>");
                    $("#result-container").replaceWith(div);
                }
            }
        })
    });

    //'like' method on a rental:
    $('body').on('click', 'a.btn-favorite', function(){
        $.ajax({
            type: "POST",
            url: '../like/',
            data: {'id': $(this).attr('name')},
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            dataType: "json",
            success: function(response) {
                //change number showing total likes
                $(this).next().children().html(response.likes_count);
                if(response.success) {
                    $(this).children('.glyphicon-star').toggleClass('active');
                }
                else  {
                    $(this).children('.glyphicon-star').removeClass('active');
                }
            },
            error: function(rs, e) {
                alert("error");
            }
        });
    })

});

// specify popup options
var customOptions = {
    "maxHeight": '200',
    'maxWidth': '250',
    'className' : 'custom-popup'
};
//generate openStreetMap using leaflet.js:
function showMap(response, markers, map) {
    //clear previous markers
    markers.clearLayers();
    var lat = [];
    var lng = [];
    if(response.length>0) {
        for (var i = 0; i < response.length; i++) {
            lat.push(response[i].coordinate[0]);
            lng.push(response[i].coordinate[1]);
        }
        var latMiddle = (Math.max.apply(null, lat) + Math.min.apply(null, lat)) / 2;
        var lngMiddle = (Math.max.apply(null, lng) + Math.min.apply(null, lng)) / 2;
        // Initialise an empty map
        map.setView([latMiddle, lngMiddle], 14);
        for (var i = 0; i < response.length; i++) {
            L.marker(response[i].coordinate)
                .bindPopup("<div class='panel panel-default'><div class='panel-heading'><h4 style='margin-bottom:10px'>$<span class='text-danger'>" +
                    response[i].price + "</span></h4></div><div class='panel-body'><a href="+
                    response[i].id +'/rental_detail/'+"><img src=" +
                    response[i].picture + " style='width:200px; height:150px;' class='img-responsive'/></a></div><div class='panel-footer'><h4 style='margin:0;'>" +
                    response[i].address + "</h4><span class='text-primary' style='margin: 0;text-align: left'><h4>" +
                    response[i].city + "</h4></span></div></div>", customOptions)
                .addTo(markers)//new markers
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

}


//create html element:
function createDiv(sortedData) {
    var div = $('<div>').attr({'class': 'col-sm-3 col-md-3', 'id': 'result-container'});
    var data = [];
    for (var i = 0; i < sortedData.length; i++) {
        data.push({
            price: sortedData[i].price,
            rental_detail: sortedData[i].id + '/rental_detail/',
            picture: sortedData[i].picture,
            address: sortedData[i].address,
            city: sortedData[i].city,
            bedroom: sortedData[i].bedroom,
            bathroom: sortedData[i].bathroom,
            like: sortedData[i].id,
            total_likes: sortedData[i].favorite_count,
            timestamp: sortedData[i].time_created
        });
    }
    $("#rentalUpdate").tmpl(data).appendTo(div);
    $("#result-container").replaceWith(div);
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

function newest(rentals) {
    rentals.sort(function(a,b){
        return new Date(a.dateTime) - new Date(b.dateTime);
    });
    return rentals;
}
