/**
 * Created by Shinjini on 4/12/2017.
 */
var skew = Skew();

$(document).ready(function(){
    var updateCorners = function(corners){
        var cornerListElt = $("#corners");
        cornerListElt.html('');
        corners.forEach(function(xy){
            var elt = $('<li>');
            elt.addClass('corner');
            elt.text('x: '+xy[0]+', y: '+xy[1]);
            cornerListElt.append(elt);
        });

    };

    $('#result-holder').click(function(e){
        var resultHolder = $(this);
        var offset = resultHolder.offset();
        var x = e.pageX - offset.left;
        var y = e.pageY - offset.top;

        skew.updatePoints([x,y]);
        updateCorners(skew.getPoints());
    });

    $('#update-corners').click(function(){
        var corners = skew.getPoints();
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
                    result.css(css);
                    $('#result-holder').append(result);
                }
            }
        });
    });


});
