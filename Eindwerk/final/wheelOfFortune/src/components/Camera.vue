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
        sockets: {
            connect: function () {
                console.log('socket connected')
            },
            customEmit: function (val) {
                console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)')
            }
        },
        methods: {
            getSockets: function () {
                self = this;
                self.$options.sockets.newRecievePeer = (data) => {
                    console.log(self.peers[data.number-1])
                    self.peers[data.number-1].signal(data.identity)

                }
            },
            streamData: function () {
                self = this;
                self.peers = [
                    new Peer(self.parameters),
                    new Peer(self.parameters),
                    new Peer(self.parameters),
                ]
                console.log('about to stream data');
                let index = 0;
                Object.keys(self.players).forEach(function (key) {
                    self.peers[index].on('signal', function (data) {
                        self.$socket.emit('newStreamPeer', {host: JSON.stringify(data), number: self.players[key].number});
                        console.log('socket shit');
                    });
                    index++;
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
            this.getSockets();
        }

    }
</script>
