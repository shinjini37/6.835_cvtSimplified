/**
 * Created by Shinjini on 4/12/2017.
 */
var skew = Skew();

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

    updateCorners(skew.getPoints());
    $('#image-holder').click(function(e){
        var imageHolder = $(this);
        var offset = imageHolder.offset();
        var x = e.pageX - offset.left;
        var y = e.pageY - offset.top;

        skew.updatePoints([x,y]);
        updateCorners(skew.getPoints());
    });

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
                    $('#result-holder').append(result);
                }
            }
        });
    });


});
