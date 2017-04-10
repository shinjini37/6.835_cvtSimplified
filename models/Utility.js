/**
 * Created by Shinjini on 11/24/2016.
 */
var Utility = function() {
    var that = Object.create(Utility);

    /**
     * Returns a millisecond representation of time in UTC
     * from https://praveenlobo.com/blog/how-to-convert-javascript-local-date-to-utc-and-utc-to-local-date/
     * because of strange problems with heroku serverside Date objects, just returns the local time for now.
     * @returns {number}
     */
    that.getTimeNowInUTC = function(){
        var now = new Date();
        // return now.getTime() + (now.getTimezoneOffset() * 60000);
        return now.getTime();
    };

    /**
     * Performs a function for all unordered combinations of elements in array,
     * ie, f(e1, e2) == f(e2, e1). Note: doesn't include (array[i], array[i]) combinations
     * @param array
     * @param fn
     */
    that.unorderedCombinations = function(array, fn){
        for (var i = 0; i < array.length; i++) {
            for (var j = i+1; j < array.length; j++) {
                fn(array[i], array[j]);
            }
        }
    };

    /**
     * Compares two arrays whose element can be compared using ==
     * Checks that elements are the same index are equal
     * @param array1
     * @param array2
     * @returns {boolean}
     */
    that.checkArraysEqualOrdered = function(array1, array2){
        if (array1.length == array2.length){
            array1.forEach(function(elt, idx){
                if (array1[idx]!=array2[idx]){
                    return false;
                }
            });
            return true;
        }
        return false;
    };

    /**
     * Compares two arrays whose element can be compared using ==
     * Checks that all elements in one are contained in the otehr
     * @param array1
     * @param array2
     * @returns {boolean}
     */
    that.checkArraysEqualUnordered = function(array1, array2){
        var matches = false;
        if (array1.length == array2.length){
            matches = true;
            array1.forEach(function(elt, idx){
                if (array2.indexOf(array1[idx]) == -1){ // since equal length, all elements present indicates equality
                    matches = false;
                }
            });
        }
        return matches;
    };

    /**
     * from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
     * Returns a random integer between min (included) and max (excluded)
     * Using Math.round() will give you a non-uniform distribution!
     * @param min
     * @param max
     * @returns {*}
     */
    that.getRandomInt = function (min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min)) + min;
    };


    Object.freeze(that);
    return that;
};

module.exports = Utility();
