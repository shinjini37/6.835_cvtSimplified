/**
 * Created by Shinjini on 4/12/2017.
 */
var Skew = function(){
    var that = Object.create(Skew.prototype);

    var origCorners = [[0,0], [0,0], [0,0], [0,0]];
    var points = [[0,0], [0,0], [0,0], [0,0]];
    var ratio = 1;

    /**
     * Inputs expected to be in app scale
     * @param width
     * @param height
     */
    that.resetCorners = function(width, height){
        if (width){
            width = width*ratio;
            height = height*ratio;
            points = [[0,0], [width,0], [width,height], [0,height]];
        } else {
            points = JSON.parse(JSON.stringify(origCorners));
        }
    };

    that.updateRatio = function(newRatio){
        ratio = newRatio;
    };

    /**
     * Inputs expected to be in app scale
     * @param newPoint
     */
    that.updatePoints = function(newPoint){
        var bestDist = Infinity;
        var bestIdx = -1;
        var corner = [newPoint[0]*ratio, newPoint[1]*ratio];

        points.forEach(function(point, idx){
            var dist = Math.pow(Math.pow((point[0]-corner[0]),2) + Math.pow((point[1]-corner[1]), 2), .5);
            if (dist<bestDist){
                bestDist = dist;
                bestIdx = idx;
            }
        });

        points[bestIdx] = corner;
    };

    that.getPoints = function(){
        return JSON.parse(JSON.stringify(points));
    };

    that.getAppScalePoints = function(){
        return points.map(function(point){
            return [point[0]/ratio, point[1]/ratio];
        });
    };


    Object.freeze(that);
    return that;
};