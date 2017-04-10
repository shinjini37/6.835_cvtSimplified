/**
 * Created by Shinjini on 11/17/2016.
 */

/**
 * This is a class to encapsulate all error handling functions.
 * @returns {ErrorHandler}
 * @constructor
 */
var ErrorHandler = function() {
    var that = Object.create(ErrorHandler);

    that.errNums = {
        // userNotInDB : [1, "User is not registered."],
        // userAlreadyInDB: [2,  "User is already registered."],
        // passwordWrongLength: [3,  "Password is not the correct length."],
        // passwordWrongCharacters: [4, "Password has invalid characters."],
        // passwordIncorrect: [5, "Incorrect Password."],
    };

    /**
     * An object to encapsulate an error generated by the app
     * TODO might need to change this to reflect how javascript errors are structured
     * @param errorNumberAndmessage
     * @returns {that.appError}
     */
    that.appError = function(errorNumberAndmessage){
        var subthat = Object.create(that.appError);
        subthat.errorNumber = errorNumberAndmessage[0];
        subthat.message = errorNumberAndmessage[1];
        Object.freeze(subthat);
        return subthat;
    };


    /**
     * Handles errors.
     *
     * @param err
     * @param res
     * TODO send only in the routes!
     */
    that.handleError = function(err, res){
        // handle the error
        var data = {}; // set later accordingly
        data.success = false;
        data.message = err.message;
        data.error = err;
        res.json(data);
    };

    Object.freeze(that);
    return that;
};

module.exports = ErrorHandler();
