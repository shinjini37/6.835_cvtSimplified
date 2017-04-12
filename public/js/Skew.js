/**
 * Created by Shinjini on 4/12/2017.
 */
var Skew = function(){
    var that = Object.create(Skew.prototype);

    var points = [[0,0], [0,0],[0,0],[0,0]];

    that.updatePoints = function(point){
        points.push(point);
        points.shift()
    };

    that.getPoints = function(){
        return JSON.parse(JSON.stringify(points));
    };


    Object.freeze(that)
    return that;
};