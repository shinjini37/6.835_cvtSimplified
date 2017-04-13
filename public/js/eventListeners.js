/**
 * Created by Shinjini on 4/12/2017.
 */
var skew = Skew();

var imgCss = {};

$(document).ready(function(){
    var updateCorners = function(corners){
        console.log(corners);
        var cornerListElt = $("#corners");
        cornerListElt.html('');
        corners.forEach(function(xy){
            var elt = $('<li>');
            elt.addClass('corner');
            elt.text('x: '+xy[0]+', y: '+xy[1]);
            cornerListElt.append(elt);
        });

    };


    var refreshImage = function(ratio, width, height){
        skew.resetCorners(width, height);
        updateCorners(skew.getPoints());
        if (ratio){
            skew.updateRatio(ratio);
        }
        $('#image-holder img').unbind().click(function(e){
            var image = $(this);
            var offset = image.offset();
            var x = e.pageX - offset.left;
            var y = e.pageY - offset.top;

            skew.updatePoints([x,y]);
            updateCorners(skew.getPoints());
        });
    };


    $('#update-corners').click(function(){
        var corners = JSON.stringify(skew.getPoints());
        console.log(corners);
        $('#result-holder').html('');
        $.ajax({
            url: '/corners',
            // Form data
            data: {corners: corners},
            type: 'POST',
            //Ajax events
            success: function (res) {
                if (JSON.parse(res.success)){
                    var result = $('<img>');
                    result.attr('src', "http://localhost:3000/images/test.png?timestamp=" + new Date().getTime());
                    result.css(imgCss);
                    $('#result-holder').append(result);
                }
            }
        });
    });

    // $("#upload-image").submit(function(event) {
    // $("#upload-image").on('input', function(event) {

    $("#file-input").on('change', function(event) {
        var fileInputElt = $(this);
        /* stop form from submitting normally */
        event.preventDefault();
        var file = fileInputElt.get(0).files[0];
        if (file){
            $('#image-holder').html('');
            $('#result-holder').html('');

            var formData = new FormData();
            formData.append('file', file);
            $.ajax({
                url: '/upload',
                // Form data
                data: formData,
                type: 'POST',
                //Ajax events
                success: function (res) {
                    if (JSON.parse(res.success)){
                        var ratio = res.ratio;
                        var height = res.height;
                        var width = res.width;
                        imgCss = {
                            height: height/ratio,
                            width: width/ratio
                        };

                        var given = $('<img>');
                        given.attr('src', "http://localhost:3000/images/image.png?timestamp=" + new Date().getTime());
                        given.css(imgCss);
                        $('#image-holder').append(given);
                        refreshImage(ratio, height, width);

                        $.ajax({
                            url: '/result',
                            type: 'GET',
                            success: function (res) {
                                if (JSON.parse(res.success)) {
                                    var result = $('<img>');
                                    result.attr('src', "http://localhost:3000/images/test.png?timestamp=" + new Date().getTime());
                                    result.css(imgCss);
                                    $('#result-holder').append(result);
                                    fileInputElt.val('');
                                }
                            }
                        });
                    }
                },
                cache: false,
                contentType: false,
                processData: false
            });
        }

    });




});
