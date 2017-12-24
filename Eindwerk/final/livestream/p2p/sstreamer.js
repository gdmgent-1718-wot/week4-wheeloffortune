let config = {
    apiKey: "AIzaSyCRDbOBN_g2rlAqy8NBSRmjfvrPMswf4EE",
    authDomain: "wheeloffyaortune2-c0e4a.firebaseapp.com",
    databaseURL: "https://wheeloffortune2-c0e4a.firebaseio.com/",
    storageBucket: "gs://wheeloffortune2-c0e4a.appspot.com/",
};
firebase.initializeApp(config);
firebase.auth().signInWithEmailAndPassword("user1@mail.be", "123456").catch(function (error) {
    // Handle Errors here.
    console.log(error.code);
    console.log(error.message);
});
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
let constraints = {audio: false, video: true};

function errorCallback(error) {
    console.log("getUserMedia error: ", error);
}

navigator.getUserMedia(constraints, function (stream) {
    let database = firebase.database()
    let Peer = require('simple-peer')
    let parameters = {
        trickle: false,
        initiator: location.hash === '#init',
        stream: stream,
    }
    let peers = [
        new Peer(parameters),
        new Peer(parameters),
        new Peer(parameters),
    ]
    let firebaseObject = {
        identity1: "null1",
        identity2: "null2",
        identity3: "null3",
    }
    let index = 0;
    Object.keys(firebaseObject).forEach(function (key) {
        peers[index].on('signal', function (data) {
            firebaseObject[key] = JSON.stringify(data)
        });
        index++;
        console.log(firebaseObject);
        database.ref('game/').update(firebaseObject);
        console.log(index);

    });
    start.onclick = function () {
        console.log('clicked');
        database.ref('game/connectie1').on('value', function (snapshot) {
            console.log(snapshot.val())
            peers[0].signal(snapshot.val())
        })

    }
    start2.onclick = function () {
        console.log('clicked');
        database.ref('game/connectie2').on('value', function (snapshot) {
            console.log(snapshot.val())
            peers[1].signal(snapshot.val())
        })

    }
    start3.onclick = function () {
        console.log('clicked');
        database.ref('game/connectie3').on('value', function (snapshot) {
            console.log(snapshot.val())
            peers[2].signal(snapshot.val())
        })

    }
    console.log('test');
}, errorCallback);


