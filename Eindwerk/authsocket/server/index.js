var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
    res.send('<marquee><h1>Server is running</h1></marquee>');
});

io.on('connection', function(socket){
    console.log('a user connected');
    socket.on('disconnect', function(){
        console.log('user disconnected');
    });
    socket.on('userInput', function(data){
        io.sockets.emit('chatMessage', data)
        // io.emit('chatMessage', data)
    });
});

http.listen(3000, function(){
    console.log('listening on *:3000');
});
