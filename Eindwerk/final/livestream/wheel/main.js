Pusher.logToConsole = true;

let pusher = new Pusher('338fc3df23a162fc1144', {
    cluster: 'eu',
    encrypted: true
});

let channel = pusher.subscribe('wheelOfFortune');

pusher.connection.bind( 'error', function( err ) {
    console.log(err.error.data)
});
channel.bind('stream', function (data) {
    console.log(data);
});

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
let constraints = { audio: false, video: true };
let video = document.querySelector("video");
function successCallback(stream) {
    video.src = window.URL.createObjectURL(stream);
}
function errorCallback(error){
    console.log("getUserMedia error: ", error);
}
navigator.getUserMedia(constraints, successCallback, errorCallback);
navigator.getUserMedia({ video: true, audio: false }, function(stream) {
    currentUser.stream = stream;
}, function() {});