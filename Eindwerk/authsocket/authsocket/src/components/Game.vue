<template>
    <div class="container">
        <h1>{{ msg }}</h1>
    </div>
</template>

<script>
    import * as firebase from "firebase";
    export default {
        name: 'Game',
        props: ['players'],
        data() {
            return {
                msg: 'Game ',
                errorCode: '',
                errorMessage: '',
                game: null,
                user: {},
                playing: false,
                answer: '',
                spots: [],
                occupied: [],
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
            clickButton: function(val){
                self = this;
                // $socket is socket.io-client instance
                this.$socket.emit('chatMessage', {message: self.answer, name: self.displayName } );
            },
            getUserData: function () {
                self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        self.user = user;


                    }
                });
            },
            getSocketData:function () {
                this.$options.sockets.chatMessage= (data) => {
                    console.log(data)
                }
            },
            authChange: function () {
                self = this
                firebase.auth().onAuthStateChanged(function(user) {
                    if (user) {
                    } else {
                        self.$router.push({name: 'Login'});
                    }
                });
            },
            getGameData: function () {
                self = this;
                firebase.database().ref('game/').on('value', function(snapshot) {
                    console.log(snapshot.val());
                    self.game = snapshot.val();
                });
            },
        }
        , mounted: function () {
            if(!players){
                console.log('what');
                this.$router.push({name: 'Lobby'});
            }
            console.log(this.players);
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
