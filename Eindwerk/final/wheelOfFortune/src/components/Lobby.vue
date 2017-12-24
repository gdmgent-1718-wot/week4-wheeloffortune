<template>
  <div>
    <header class="align-items container-fluid red-bg">
      <div class="align-center">
        <h1>{{ msg }}</h1>
      </div>
    </header>
    <main class="container-fluid">
      <div class="small-container pt-2">
        <div class="spots inline-block" v-if="spots && !playing">
          <h2 class="pb-1">Beschikbare plaatsen:</h2>
          <div v-for="(spot, index) in spots" class="card mb-1 col-4">
            <h3 class="">Speler {{spot.number}}</h3>
            <button class="btn btn-info" v-on:click="claimSpot(spot.number)">Eis plaats op</button>
          </div>
        </div>
        <div v-if="occupied" class="occupied pt-3 inline-block">
          <hr>
          <p class="text-info" v-if="occupied && playing" >The game will start soon waiting for {{spots.length}} more players</p>
          <h2 v-if="occupied" class="pb-1">Huidige spelers aan het wachten:</h2>
          <div v-for="player in occupied" class="card">
            <h3 class="pb-1 pt-2">{{player.name}}</h3>
          </div>
        </div>
      </div>
    </main>
  </div>
    <!--<div class="container">-->
        <!--<h1>{{ msg }}</h1><hr>-->
        <!--<div class="spots" v-if="spots && !playing">-->
            <!--<h2 class="pb-3">Available spots:</h2>-->
            <!--<div v-for="(spot, index) in spots" class="card mb-3">-->
                <!--<h3 class="pb-1 pt-3">Player {{spot.number}}</h3>-->
                <!--<button class="btn btn-info" v-on:click="claimSpot(spot.number)">Claim spot</button>-->
            <!--</div><hr>-->
        <!--</div>-->
        <!--<div v-if="occupied" class="occupied">-->
            <!--<p class="text-info" v-if="occupied && playing" >The game will start soon waiting for {{spots.length}} more players</p>-->
            <!--<h2 v-if="occupied" class="pb-3 pt-1">Current players:</h2>-->
            <!--<div v-for="player in occupied" class="card mb-3">-->
                <!--<h3 class="pb-1 pt-2">{{player.name}}</h3>-->
            <!--</div>-->
        <!--</div>-->
    <!--</div>-->
</template>

<script>
    import * as firebase from "firebase";
    import vuesocket from "vue-socket.io";

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
                let self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        self.user = user;
                    }
                });
            },
            authChange: function () {
                let self = this
                firebase.auth().onAuthStateChanged(function(user) {
                    if (user) {
                    } else {
                        self.$router.push({name: 'Login'});
                    }
                });
            },
            getGameData: function () {
                let self = this;
                console.log('lalal');
                firebase.database().ref('game/players').on('value', function(snapshot) {
                    console.log(snapshot.val());
                    self.game = snapshot.val();
                    self.checkSpot();

                });
            },
            checkSpot: function () {
                let self = this
                self.spots = [];
                self.occupied = [];
                for (let player of Object.values(self.game)) {
                    if(player.id === self.user.uid){
                        self.playing = true
                        self.occupied.push(player)
                        console.log(self.occupied);
                        if(self.occupied.length === 3 ){
                          firebase.database().ref('game/finished/').update({
                            end: false,
                            winner: 'test'
                          });
                            console.log('start the game')
                            this.$socket.emit('startGame')
                            self.$router.push({ name: 'GameFinal',})


                        }
                    }else {
                        if(!player.playing){
                            self.spots.push(player);
                        }else {
                            self.occupied.push(player);
                            console.log(self.occupied);
                            if(self.occupied.length === 3){
                                console.log('start the game')
                              firebase.database().ref('game/finished/').update({
                                end: false,
                                winner: 'test'
                              });
//                                firebase.database().ref('game/lettersUsed/').set(null);
                                this.$socket.emit('startGame')
                                self.$router.push({ name: 'GameFinal', })
                            }
                        }
                    }

                }
            },
            claimSpot: function (number) {
                let self = this;
                let selector = "player"+(number);
                console.log(selector);
                firebase.database().ref('game/players/'+selector).update({
                    id: self.user.uid ,
                    name: self.user.displayName,
                    playing: true,
                });
//                firebase.database().ref('game/players/'+selector).on('value', function(snapshot) {
//                    console.log(snapshot.val());
//                });
//                self.playing = true
                self.checkSpot();
            }
        }
        , mounted: function () {
            this.authChange();
            this.getUserData();
            this.getGameData();
            //this.getSocketData();

        }
    }
</script>
