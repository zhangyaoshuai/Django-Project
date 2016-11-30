/**
 * Created by EricZhang on 11/28/16.
 */
$(document).ready(function () {
    $('#searchForm').on('submit', function (e) {
        //e.preventDefault();
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
});