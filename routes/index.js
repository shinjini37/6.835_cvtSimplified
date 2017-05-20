/**
 * Created by Shinjini on 12/10/2016.
 */

var express = require('express');
var router = express.Router();
//var UserModel = require('../models/User');

//var errorHandler = require('../models/ErrorHandler');
//var response = require('../models/Response');

//https://github.com/extrabacon/python-shell
var PythonShell = require('python-shell');

var fs = require('fs');
var path = require('path');

var multer = require('multer');

var upload = multer({ dest: './temp'});

var RATIO = 600/400;

var runPython = function(scriptName, inputs, onMessage, onDone){
    var pyshell = new PythonShell(scriptName, { mode: 'text'});
    inputs.forEach(function(input){
        pyshell.send(input);
    });
    pyshell.on("message", function(message){
        if (onMessage){
            onMessage(message);
        }
    });
    pyshell.end(function (err) {
        if (onDone){
            onDone(err);
        }
    });
};

router.post('/test', function(req, res, next){
    var messages = [];
    var makeOnMessageFunction = function(messages){
        var onMessage = function(message){
            console.log(message);
            message = JSON.parse(message.trim());
            messages.push(message);
        };
        return onMessage
    };

    var onDone = function(){
        res.json({success:true, messages:messages});
    };

    runPython('python/smolTest.py', [], makeOnMessageFunction(messages), onDone);
});
// router.post('/test', function(req, res, next){
//
// });

// File input field name is simply 'file'
router.post('/upload', upload.single('file'), function(req, res, next) {
    console.log('got here at least');
    var tempPath = req.file.path;
    console.log(tempPath);
    // var ext = path.extname(req.file.originalname).toLowerCase();
    // var targetPath = path.resolve('python/image.'+ext);
    var targetPath = path.resolve('./python/image.png');

    console.log(targetPath);
    console.log(1);
    fs.rename(tempPath, targetPath, function(err) {
        console.log(2);
        if (err) throw err;
        var scriptName = './python/write_to_public.py';
        var inputs = ['./python/image.png'];
        var height = 0;
        var width = 0;
        var onMessage = function(message){
            console.log('message: ', message);
            message = message.trim();
            var messageComps = message.split(',');
            console.log(messageComps);
            if (messageComps[0] == "width"){
                width = parseInt(messageComps[1]);
            } else if (messageComps[0] == "height") {
                height = parseInt(messageComps[1]);
            }
            console.log(1, width, height);
        };
        runPython(scriptName, inputs, onMessage, function(err){
            if (err) console.log(err);
            console.log(2, width, height);
            res.json({success:true, ratio: RATIO, height: height, width: width});
        });
    });
});

router.get('/result', function(req, res, next) {
    console.log('got here at least 2 ');
    var scriptName = './python/main.py';
    var inputs = ['./python/image.png', 'None'];
    var messages = [];
    var makeOnMessageFunction = function(messages){
        var onMessage = function(message){
            console.log(message);
            message = JSON.parse(message.trim());
            messages.push(message);
        };
        return onMessage
    };

    var onDone = function(err){
        if (err) console.log(err);
        console.log('finished');
        res.json({success:true, messages:messages});
    };

    runPython(scriptName, inputs, makeOnMessageFunction(messages), onDone);

});

router.post('/corners', function(req, res, next) {
    console.log('got here at least 3 ');
    var corners = req.body.corners || "None";
    console.log(req.body);
    console.log(corners);
    var scriptName = './python/main.py';
    var inputs = ['./python/image.png', corners];
    var messages = [];
    var makeOnMessageFunction = function(messages){
        var onMessage = function(message){
            console.log(message);
            message = JSON.parse(message.trim());
            messages.push(message);
        };
        return onMessage
    };

    var onDone = function(err){
        if (err) console.log(err);
        console.log('finished');
        res.json({success:true, messages:messages});
    };

    runPython(scriptName, inputs, makeOnMessageFunction(messages), onDone);

});


//
// /**
//  * Signup a new user, and sets them as the logged in user
//  * If the user is already present, send the error to be handled in the errorHandler
//  */
// router.post('/signup', function(req, res, next) {
//     var username = req.body.username.toLowerCase();
//     var password = req.body.password;
//     var email = req.body.email;
//     var publicEmail = req.body.publicEmail;
//     UserModel.addUser(username, password, email, publicEmail, function(err, user){
//         if (err){
//             errorHandler.handleError(err, res);
//         } else {
//             req.session.loggedInUsername = user.username;
//             req.session.loggedInUserId = user._id; // speeds certain things up
//             response.handleResponse({username: user.username}, res);
//         }
//     });
// });
//
// /**
//  * Check if the session has a user signed in
//  */
// router.get('/signin', function(req, res, next){
//     if (req.session.loggedInUsername){
//         response.handleResponse({username: req.session.loggedInUsername}, res);
//     } else {
//         errorHandler.handleError(notLoggedInError, res);
//     }
// });
//
// /**
//  * Logs in a user by setting them as the logged in user
//  * If the user is not present in the DB, send the error to be handled in the errorHandler.
//  * If the password is incorrect, sends an error to be handled in the errorHandler.
//  */
// router.post('/signin', function(req, res, next) {
//     var username = req.body.username.toLowerCase();
//     var password = req.body.password;
//
//     if (!req.session.loggedInUsername){
//         UserModel.getUser(username, function(err, user){
//             if (err){
//                 errorHandler.handleError(err, res);
//             } else {
//                 bcrypt.compare(password, user.passwordHash, function(err, matches) {
//                     if (err){
//                         errorHandler.handleError(err, res);
//                     } else {
//                         if (matches){ // matches
//                             req.session.loggedInUsername = user.username;
//                             req.session.loggedInUserId = user._id; // speeds certain things up
//                             response.handleResponse({username: user.username}, res);
//                         } else {
//                             errorHandler.handleError(
//                                 errorHandler.appError(errorHandler.errNums.passwordIncorrect),
//                                 res);
//                         }
//                     }
//                 });
//             }
//         });
//     } else {
//         errorHandler.handleError(
//             errorHandler.appError(errorHandler.errNums.alreadyLoggedIn),
//             res);
//     }
//
// });
//
// /**
//  * Signs out the user by deleting the logged in user
//  */
// router.post('/signout', function(req, res, next) {
//     delete req.session.loggedInUsername;
//     delete req.session.loggedInUserId;
//     response.handleResponse({}, res);
// });
//


module.exports = router;
