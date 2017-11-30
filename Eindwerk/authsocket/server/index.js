var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var admin = require("firebase-admin");

var serviceAccount = require("./account/wheeloffortune2-c0e4a-firebase-adminsdk-xx83k-e44ffb01f2.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://wheeloffortune2-c0e4a.firebaseio.com/"
});

// Attach an asynchronous callback to read the data at our posts reference


app.get('/', function (req, res) {
    res.send('<marquee><h1>Server is running</h1></marquee>');
});
var db = admin.database();
var ref = db.ref("game");
ref.on("value", function (snapshot) {
    data = snapshot.val();
    checkConnection(data);
}, function (errorObject) {
    console.log("The read failed: " + errorObject.code);
});
function checkConnection(data) {
    var nsp = io.of('/' + data.room);
    nsp.on('connection', function (socket) {
        console.log('someone connected');
        socket.on('disconnect', function () {
            console.log('user disconnected');
        });
        socket.on('turnChange', function (data) {
            console.log(data);
            nsp.emit('turnChange', data)
        });
        socket.on('answer', function (data) {
            console.log(data);
            // nsp.sockets.emit('turnChange', data)
        });

    });
}

// nsp.emit('hi', 'everyone!');
//
// io.on('connection', function(socket){
//     console.log('a user connected');
//     socket.on('disconnect', function(){
//         console.log('user disconnected');
//     });
//     socket.on('userInput', function(data){
//         io.sockets.emit('chatMessage', data)
//         // io.emit('chatMessage', data)
//     });
// });

http.listen(3000, function () {
    console.log('listening on *:3000');
});
