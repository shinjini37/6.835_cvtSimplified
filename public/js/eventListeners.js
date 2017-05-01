/**
 * Created by Shinjini on 4/12/2017.
 */
var skew = Skew();

var imgCss = {};

$(document).ready(function(){
    var inputCanvas = InputCanvas($('#input-canvas'));
    var resultCanvas = InputCanvas($('#result-canvas'));

    var updateCorners = function(corners){
        console.log(corners);
        var cornerListElt = $("#corners");
        cornerListElt.html('');
        corners.forEach(function(xy){
            console.log(xy);
            var elt = $('<li>');
            elt.addClass('corner');
            elt.text('x: '+xy[0]+', y: '+xy[1]);
            cornerListElt.append(elt);
        });
        inputCanvas.clear();
        inputCanvas.drawPoints(corners);

    };

    var processMessages = function(messages){
        var corners = messages[0];
        var lines = messages[1];
        var circles = messages[2];
        console.log(corners);

        corners.forEach(function(corner){
            skew.updatePoints(corner, true);
        });
        updateCorners(skew.getAppScalePoints());
        var ratio = skew.getRatio();
        //resultCanvas.clear();
        //resultCanvas.drawLines(lines, ratio);
        //resultCanvas.drawCircles(circles, ratio);
    };

    var refreshImage = function(ratio, width, height){
        if (ratio){
            skew.updateRatio(ratio);
        }
        skew.resetCorners(width, height);
        inputCanvas.updateCanvasDimensions(width, height);
        resultCanvas.updateCanvasDimensions(width, height);
        updateCorners(skew.getAppScalePoints());
        $('#image-holder img').unbind().click(function(e){
            var image = $(this);
            var offset = image.offset();
            var x = e.pageX - offset.left;
            var y = e.pageY - offset.top;

            skew.updatePoints([x,y]);
            updateCorners(skew.getAppScalePoints());
        });
    };


    $('#update-corners').click(function(){
        var corners = JSON.stringify(skew.getPoints());
        console.log(corners);
        $('#result-holder').html('');
        $.ajax({
            url: '/corners',
            data: {corners: corners},
            type: 'POST',
            //Ajax events
            success: function (res) {
                if (JSON.parse(res.success)){
                    var messages = res.messages;
                    processMessages(messages);

                    var result = $('<img>');
                    result.attr('src', "http://localhost:3000/images/result.png?timestamp=" + new Date().getTime());
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
            $('#image-holder img').remove();
            $('#result-holder img').remove();
            inputCanvas.clear();
            resultCanvas.clear();
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
                        var height = res.height/ratio;
                        var width = res.width/ratio;
                        imgCss = {
                            height: height,
                            width: width
                        };

                        var given = $('<img>');
                        given.attr('src', "http://localhost:3000/images/image.png?timestamp=" + new Date().getTime());
                        given.css(imgCss);
                        $('#image-holder').append(given);
                        refreshImage(ratio, width, height);

                        $.ajax({
                            url: '/result',
                            type: 'GET',
                            success: function (res) {
                                if (JSON.parse(res.success)) {
                                    var messages = res.messages;
                                    processMessages(messages);
                                    var result = $('<img>');
                                    result.attr('src', "http://localhost:3000/images/result.png?timestamp=" + new Date().getTime());
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
