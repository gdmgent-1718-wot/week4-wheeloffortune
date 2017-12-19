// import Pusher from 'pusher';
var Pusher = require('pusher');
var app = require('express')();
var http = require('http').Server(app);

app.get('/', function (req, res) {
    res.send('<marquee><h1>Server is running</h1></marquee>');
});
let pusher = new Pusher({
    appId: '444197',
    key: '338fc3df23a162fc1144',
    secret: '77ef4433a16e0ae513b8',
    cluster: 'eu',
    encrypted: true
});

pusher.trigger('wheelOfFortune', 'stream', {"message": "hello world"});
http.listen(3000, function(){
    console.log('listening on *:3000');
});
