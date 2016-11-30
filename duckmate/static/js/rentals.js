$(document).ready(function() {

    //global variable:
    var dump = [];
    var response = [];

    //initialize map:
    var map = L.map('map');
    var mytiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });
    map.addLayer(mytiles);
    var markers = new L.LayerGroup().addTo(map);

    //asyncronously getting backend json data from url: showIndex
    $.ajax({
        url: '../getRentals/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        success: function(data) {
            response = data.features;//json data from backend
            dump = response;
            showMap(response, markers, map);

        },
        failure: function(data) {
            alert('Got an error!');
        }
    });
    //sort by price low to high:
    $("#priceLowToHigh").click(function () {
        sortedData = priceLowToHigh(response);
        var div = $('<div>').attr({'class': 'col-sm-3 col-md-3',
                                    'id': 'result-container'});
        for (var i = 0; i < sortedData.length; i++) {
            createDiv(div, sortedData, i);
        }
        $("#result-container").replaceWith(div);


    });

    //sort by price high to low:
    $("#priceHighToLow").click(function () {
        sortedData = priceHighToLow(response);
        var div = $('<div>').attr({'class': 'col-sm-3 col-md-3',
                                    'id': 'result-container'});
        for (var i = 0; i < sortedData.length; i++) {
            createDiv(div, sortedData, i);
        }
        $("#result-container").replaceWith(div);


    });
    //sort by time created:
    $("#newest").click(function () {
        sortedData = newest(response);
        var div = $('<div>').attr({'class': 'col-sm-3 col-md-3',
                                    'id': 'result-container'});
        for (var i = 0; i < sortedData.length; i++) {
            createDiv(div, sortedData, i);
        }
        $("#result-container").replaceWith(div);
    });

    //filter by price:
    $("#searchPrice").click(function () {
        response = dump;
        var min_price = $("#min_price").val();
        console.log(min_price);
        var max_price = $("#max_price").val();
        if(min_price == '') {
            min_price = 0;
        }
        if(max_price == '') {
            max_price = 5000;
        }
        var result = [];
        var div = $('<div>').attr({'class': 'col-sm-3 col-md-3',
                                    'id': 'result-container'});
        for (var i=0; i<response.length; i++) {
            if(response[i].price>=min_price && response[i].price<=max_price) {
                result.push(response[i]);
                createDiv(div, response, i);
            }
        }
        showMap(result, markers, map);
        $("#result-container").replaceWith(div);
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
                var result = data.features;
                response = result;
                dump = response;
                showMap(result, markers, map);
                if (result.length>0) {
                    var div = $('<div>').attr({'class': 'col-sm-3 col-md-3',
                                    'id': 'result-container'});
                    for (var i = 0; i < result.length; i++) {
                        createDiv(div, result, i);
                    }
                    $("#result-container").replaceWith(div);
                }
                else {
                    var div = $('<div>').attr({'class': 'col-sm-3 col-md-3',
                                    'id': 'result-container'});
                    div.append("<div class='alert alert-warning'><p style='text-align: center'><strong>No results</strong></p></div>");
                    $("#result-container").replaceWith(div);
                }
            }
        })
    });

    //click on input field to clear it:
    $("input").focus(function () {
		$(this).val('');
	});

    //like button on click:
    $('.btn-favorite').click(function(){
        $.ajax({
            type: "POST",
            url: '../like/',
            data: {'id': $(this).attr('name')},
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            dataType: "json",
            success: function(response) {
                alert(response.message);
                alert('Rental likes count is now ' + response.likes_count);
                $(this).children('.glyphicon-star').toggleClass('active');
            },
            error: function(rs, e) {
                alert("error");
            }
        });
    })

});


//generate openstreetmap using leaflet.js:
function showMap(response, markers, map) {
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
                .bindPopup("<div class='caption'><h4 style='margin-bottom:10px'>$<span class='text-danger'>" +
                    response[i].price + "</span></h4></div><a href="+
                    response[i].id +'/rental_detail/'+"><img src=" +
                    response[i].picture + " style='width:200px; height:150px;' class='img-rounded'/></a><div class='caption'><h4 style='margin:0;'>" +
                    response[i].address + "</h4><span class='text-primary' style='margin: 0;text-align: left'><h4>" +
                    response[i].city + "</h4></span></div>")
                .addTo(markers)
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
function createDiv(div, sortedData, i) {
    div.append("<div class='panel panel-default' style='margin: 0; padding: 0;'><div class='panel-heading'><h4 class='text-primary'>$"+
        sortedData[i].price +"</h4></div><div class='panel-body'>" +
        "<a href="+sortedData[i].id+'/rental_detail/'+"><img src=" +
        sortedData[i].picture + " style='height: 250px; width: 100%; margin: 0; padding: 0'>" +
        "</a></div><div class='panel-footer'><h5 style='margin:0'> <span class='text-primary' style='margin: 0;text-align: left'>" +
        sortedData[i].address + "</span></h5> <span style='margin: 0;text-align: right'>" +
        sortedData[i].city + "</span> <span class='text-danger'>" +
        sortedData[i].bedroom + "bed/" +
        sortedData[i].bathroom + "bath</span></span> <a href="+
        sortedData[i].id +'/rental_detail/' +" class='btn btn-primary btn-sm' role='button'>View Details</a><a name="+
        sortedData[i].id +" class='btn btn-default btn-sm btn-favorite' role='button'><span class='glyphicon glyphicon-star'></span></a> <span><small>"+
        sortedData[i].favorite_count +"</small></span><small class='pull-right text-primary'>"+
        sortedData[i].time_created +"</small>" +
        "</div></div>")

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
