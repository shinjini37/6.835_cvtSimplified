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

    that.drawPoints = function(points){
        var context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height)
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



    Object.freeze(that);
    return that;
};