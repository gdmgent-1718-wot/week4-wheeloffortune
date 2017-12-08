<template>
    <div class="container">
        <h1>{{ msg }}</h1>
        <div class="game">
            <div v-if="currentAnswer">
                <h5>currentAnswer</h5>
                <p>player: {{currentAnswer.player}}</p>
                <p>answer: {{currentAnswer.answer}}</p>
            </div>
            <div v-if="players && currentPlayer" v-for="player in players" class="players">
                <div  v-if="player.id == currentPlayer.id" class="currentPlayer">
                    <h3 style="font-weight: bold">{{player.name}}</h3>
                    <div v-if="player.active" class="playing">
                        <p>Playing</p>
                        <button v-on:click="endTurn">End Turn</button>
                        <div class="answer">
                            <input type="text" name="answer" v-model="answer">
                            <button v-on:click="sendAnswer">send</button>
                        </div>
                    </div>
                    <p v-else="!player.active">Waiting</p>
                </div>
                <div v-else="player.id != currentPlayer.id" class="otherPlayer">
                    <h3>{{player.name}}</h3>
                    <p v-if="player.active">Playing</p>
                    <p v-else="!player.active">Waiting</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue'
    import * as firebase from "firebase";
    import VueSocketio from 'vue-socket.io';
    Vue.use(VueSocketio, 'http://localhost:3000/');


    export default {
        name: 'Game',
        data() {
            return {
                msg: 'Game ',
                errorCode: '',
                errorMessage: '',
                game: null,
                user: {},
                active: false,
                answer: '',
                players: [],
                currentPlayer: null,
                currentAnswer: null,
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
            getUserData: function () {
                self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        self.user = user;
                    }
                });
            },
            getSocketData: function () {
                self = this;
                self.$options.sockets.turnChange = (data) => {
                    console.log(data)
                }
                self.$options.sockets.answer = (data) => {
                    self.currentAnswer = data;
                }
            },
            sendAnswer: function () {
                this.$socket.emit('answer', {player: this.currentPlayer.name, answer: this.answer});
                this.endTurn();
                this.answer = null;
            },
            authChange: function () {
                self = this
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                    } else {
                        self.$router.push({name: 'Login'});
                    }
                });
            },
            getGameData: function () {
                self = this;

                firebase.database().ref('game').on('value', function (snapshot) {
                    console.log(snapshot.val());
                    self.game = snapshot.val();
                    self.getPlayers(self.game.players)
//                    self.connectToSocket();
                })
            },
            getPlayers: function (players) {
                console.log(this.game);
                self = this;
                self.players=[];
                self.currentPlayer=[];
                for (let player of Object.values(players)) {

                    if (player.id === self.user.uid) {
                        self.currentPlayer = player;
                        self.players.push(player)
                    }
                    else {
                        if (player.playing) {
                            self.players.push(player);
                        }
                    }
                }
            },
            endTurn: function () {
                console.log(this.currentPlayer);
                this.$socket.emit('turnChange', {number: this.currentPlayer.number});
            },

        },
        mounted: function () {
            this.authChange();
            this.getUserData();
            this.getGameData();
            this.getSocketData();
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    h1, h2 {
        font-weight: normal;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }
</style>
