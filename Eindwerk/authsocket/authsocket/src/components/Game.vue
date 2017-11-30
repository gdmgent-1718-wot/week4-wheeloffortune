<template>
    <div class="container">
        <h1>{{ msg }}</h1>
        <div class="game">
            <div v-if="players && currentPlayer" v-for="player in players" class="players">
                <div  v-if="player.id == currentPlayer.id" class="currentPlayer">
                    <h3 style="font-weight: bold">{{player.name}}</h3>
                    <div v-if="player.active" class="playing">
                        <p >Playing</p>
                        <button v-on:click="endTurn">End Turn</button>
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
    import * as firebase from "firebase";

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
            clickButton: function (val) {
                self = this;
                // $socket is socket.io-client instance
                this.$socket.emit('chatMessage', {message: self.answer, name: self.displayName});
            },
            getUserData: function () {
                self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        self.user = user;
                    }
                });
            },
            getSocketData: function () {
                this.$options.sockets.chatMessage = (data) => {
                    console.log(data)
                }
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
                console.log('hallo');
                self = this;
                firebase.database().ref('game/players/').on('value', function (snapshot) {
                    self.game = snapshot.val();
                    self.getPlayers();
                });
            },
            getPlayers: function () {
                self = this;
                self.players=[];
                self.currentPlayer=[];
                for (let player of Object.values(self.game)) {

                    if (player.id === self.user.uid) {
                        self.currentPlayer = player;
                        self.players.push(player)
                        console.log(self.players);
                        console.log(self.currentPlayer);
                    }
                    else {
                        console.log('notfound')
                        if (player.playing) {
                            self.players.push(player);
                            console.log(self.players);
                            console.log(self.currentPlayer);
                        }
                    }
                }
            },
            endTurn: function () {
                console.log("ending turn");
            },

        }
        , mounted: function () {
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
