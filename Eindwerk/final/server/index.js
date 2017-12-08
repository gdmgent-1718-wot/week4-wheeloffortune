var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var admin = require("firebase-admin");

var serviceAccount = require("./account/wheeloffortune2-c0e4a-firebase-adminsdk-xx83k-e44ffb01f2.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://wheeloffortune2-c0e4a.firebaseio.com/"
});

app.get('/', function (req, res) {
    res.send('<marquee><h1>Server is running</h1></marquee>');
});
function getGameData() {
    var db = admin.database();
    var ref = db.ref("game");
    self  = this;
    return ref.on("value", function (snapshot) {
        console.log('hallo');
        return snapshot.val();
    }, function (errorObject) {
        console.log("The read failed: " + errorObject.code);
    });
}
function changeActivePlayer(currentPlayer, newPlayer) {
    admin.database().ref('game/players/player'+currentPlayer).update({
        active: false,
    });
    admin.database().ref('game/players/player'+newPlayer).update({
        active: true,
    });
}
io.on('connection', function (socket) {
    console.log('someone connected');
    socket.on('disconnect', function () {
        console.log('user disconnected');
    });
    socket.on('turnChange', function (data) {
        console.log(data);
        var num = parseInt(data.number);
        if(num === 3){
            num = 1;
            console.log(num);
            io.emit('turnChange', {'number': num})
            changeActivePlayer(data.number, num)
        }else{
            num++;
            console.log(num);
            io.emit('turnChange', {'number': num})
            changeActivePlayer(data.number, num)

        }
    });
    socket.on('answer', function (data) {
        console.log(data);
        io.emit('answer', data)
    });
});


http.listen(3000, function () {
    console.log('listening on *:3000');
});
