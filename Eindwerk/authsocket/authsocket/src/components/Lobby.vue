<template>
    <div class="container">
        <h1>{{ msg }}</h1>
        <div class="spots" v-if="spots && !playing">
            <h1>Available spots:</h1>
            <div v-for="(spot, index) in spots" class="card">
                <h1>player {{spot.number}}</h1>
                <button v-on:click="claimSpot(spot.number)">Claim Spot</button>
            </div>
        </div>
        <div v-if="occupied && playing" class="occupied">
            <h1 >The game will start soon waiting for {{spots.length}} more players</h1>
            <h2>current players:</h2>
            <div v-for="player in occupied" class="card">
                <h3>{{player.name}}</h3>
            </div>
        </div>
    </div>
</template>

<script>
    import * as firebase from "firebase";
    export default {
        name: 'Lobby',
        data() {
            return {
                msg: 'Lobby ',
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
        methods: {
            getUserData: function () {
                self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        self.user = user;
                    }
                });
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
                    self.checkSpot();

                });
            },
            checkSpot: function () {
                self = this
                self.spots = [];
                self.occupied = [];
                for (let player of Object.values(self.game)) {
                    if(player.id === self.user.uid){
                        self.playing = true
                        self.occupied.push(player)
                        console.log(self.occupied);
                        if(self.occupied.length === 3 ){
                            console.log('start the game')
                            self.$router.push({name: 'Game', players: self.occupied});

                        }
                    }else {
                        if(!player.playing){
                            self.spots.push(player);
                        }else {
                            self.occupied.push(player);
                            console.log(self.occupied);
                            if(self.occupied.length === 3){
                                console.log('start the game')
                                self.$router.push({name: 'Game', players: self.occupied});

                            }
                        }
                    }

                }
            },
            claimSpot: function (number) {
                self = this;
                let selector = "player"+(number);
                console.log(selector);
                firebase.database().ref('game/'+selector).update({
                    id: self.user.uid ,
                    name: self.user.displayName,
                    playing: true,
                });
                self.playing = true
                self.checkSpot();
            }
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
