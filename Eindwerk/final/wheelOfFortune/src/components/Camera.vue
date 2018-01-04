<template>
    <div>
        <video autoplay></video>
        <div id="colorPicker"></div>
    </div>
</template>

<script>
    import Vue from 'vue'
    import * as firebase from "firebase";
    import Peer from 'simple-peer';
    import VueSocketio from 'vue-socket.io';

    Vue.use(VueSocketio, 'http://localhost:3000/');

    export default {
        name: 'Camera',
        data() {
            return {
                video: null,
                constraints: {audio: false, video: true},
                database: firebase.database(),
                parameters: {
                    trickle: false,
                    initiator: true,
                    stream: null,
                },
                peers: null,
                firebaseObject: null,
                players: null,

            }
        },
        methods: {
            startStream: function () {
                console.log('hello');
                let index = 0;
                Object.keys(self.players).forEach(function (key) {
                    if (self.players[key].identity !== 0) {
                            self.peers[index].signal(self.players[key].identity)
                    }
                    index++;
                })
            },
            streamData: function () {
                self = this;
                self.peers = [
                    new Peer(self.parameters),
                    new Peer(self.parameters),
                    new Peer(self.parameters),
                ]
                let index = 0;
                Object.keys(self.players).forEach(function (key) {
                    self.peers[index].on('signal', function (data) {
                        console.log('ffuck')
                        if (self.players[key].host === 0) {
                            self.database.ref('game/players/' + key).update({host: JSON.stringify(data)})
                        }
                    })
                    index++
                    if (index === 2) {
                        self.startStream()
                    }

                })
            },
            checkPeers: function () {
                self = this;
                self.database.ref('game/players').on('value', function (snapshot) {
                    self.players = snapshot.val();

                    let playing = 0;
                    Object.keys(snapshot.val()).forEach(function (key) {
                        if (self.players[key].playing) {
                            ++playing
                            if (playing === 3) {
                                self.streamData();
                            }
                        }
                    })

                });

            },
            getVideo: function () {
                self = this;
                navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
                self.video = document.querySelector("video");

                navigator.getUserMedia(this.constraints, function (stream) {
                    self.video.src = window.URL.createObjectURL(stream);
                    self.parameters.stream = stream;
                    self.checkPeers();
                }, function (error) {
                    console.log("getUserMedia error: ", error);
                });
            }
        },

        mounted() {
            this.getVideo();
        }

    }
</script>
