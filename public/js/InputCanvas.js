/**
 * Created by Shinjini on 4/12/2017.
 */

var InputCanvas = function(canvasElt){
    var that = Object.create(InputCanvas.prototype);
    var canvas = canvasElt[0];

    that.updateCanvasDimensions = function(width, height){
        canvas.width = width;
        canvas.height = height;
    };

    that.clear = function(){
        var context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);

    };

    that.drawPoints = function(points){
        var context = canvas.getContext('2d');
        points.forEach(function(point){
            var radius = 3;
            context.beginPath();
            context.arc(point[0], point[1], radius, 0, 2 * Math.PI, false);
            context.fillStyle = '#D2A8FF';
            context.fill();
            context.lineWidth = 2;
            context.strokeStyle = '#75519C';
            context.stroke();
            context.closePath();
        });
    };

    that.drawCircles = function(circles, ratio){
        ratio = ratio || 1;
        var context = canvas.getContext('2d');
        circles.forEach(function(circle){
            var x = circle[0]/ratio;
            var y = circle[1]/ratio;
            var cent_radius = 3;
            var radius = circle[2]/ratio;
            context.beginPath();
            context.arc(x, y, radius, 0, 2 * Math.PI, false);
            context.strokeStyle = 'red';
            context.stroke();
            context.closePath();

            context.beginPath();
            context.arc(x, y, cent_radius, 0, 2 * Math.PI, false);
            context.fillStyle = 'blue';
            context.fill();
            context.closePath();
        });
    };

    that.drawLines = function(lines, ratio){
        ratio = ratio || 1;

        var context = canvas.getContext('2d');
        lines.forEach(function(line){
            var xy1 = line[0];
            var xy2 = line[1];
            context.beginPath();
            context.moveTo(xy1[0]/ratio, xy1[1]/ratio);
            context.lineTo(xy2[0]/ratio, xy2[1]/ratio);
            context.strokeStyle = 'green';
            context.stroke();
            context.closePath();
        });
    };

    Object.freeze(that);
    return that;
};