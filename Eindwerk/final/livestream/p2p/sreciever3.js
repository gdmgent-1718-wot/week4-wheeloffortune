let Peer = require('simple-peer')
let peer = new Peer({
    trickle: false
});
let config = {
    apiKey: "AIzaSyCRDbOBN_g2rlAqy8NBSRmjfvrPMswf4EE",
    authDomain: "wheeloffyaortune2-c0e4a.firebaseapp.com",
    databaseURL: "https://wheeloffortune2-c0e4a.firebaseio.com/",
    storageBucket: "gs://wheeloffortune2-c0e4a.appspot.com/",
};
firebase.initializeApp(config);
firebase.auth().signInWithEmailAndPassword("user2@mail.be", "123456").catch(function(error) {
    // Handle Errors here.
    console.log(error.code);
    console.log(error.message);
});
let database = firebase.database()
let start = document.getElementById("start");

start.onclick = function () {
    console.log('clicked');
    database.ref('game/identity3').on('value', function (snapshot) {
        console.log(snapshot.val())
        peer.signal(snapshot.val())
    })

}

peer.on('signal', function (data) {
    console.log(JSON.stringify(data));
    database.ref('game/').update({
        connectie3 : JSON.stringify(data)
    });
})
peer.on('stream', function (stream) {
    let video = document.createElement('video');
    document.body.appendChild(video);
    video.src = window.URL.createObjectURL(stream);
    video.play();

})
console.log('test');