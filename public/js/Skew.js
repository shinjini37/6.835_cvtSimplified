/**
 * Created by Shinjini on 4/12/2017.
 */
var Skew = function(){
    var that = Object.create(Skew.prototype);

    var origCorners = [[0,0], [0,0], [0,0], [0,0]];
    var points = [[0,0], [0,0], [0,0], [0,0]];
    var ratio = 1;

    that.resetCorners = function(width, height){
        if (width){
            points = [[0,0], [width,0], [width,height], [height,0]];
        } else {
            points = JSON.parse(JSON.stringify(origCorners));
        }
    };

    that.updateRatio = function(newRatio){
        ratio = newRatio;
    };

    that.updatePoints = function(point){
        var corner = [point[0]*ratio, point[1]*ratio];
        points.push(corner);
        points.shift()
    };

    that.getPoints = function(){
        return JSON.parse(JSON.stringify(points));
    };


    Object.freeze(that);
    return that;
};