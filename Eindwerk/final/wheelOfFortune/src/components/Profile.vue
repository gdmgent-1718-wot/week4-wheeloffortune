<template>
  <div>
    <header class="align-items container-fluid red-bg">
      <div class="align-center">
        <h1>{{ msg }}</h1>
      </div>
    </header>
    <main class="container-fluid">
      <div class="small-container pt-2">
        <p>
          Raad een letter uit een zin, woord of gezegde, als u het juist heeft mag u nog eens draaien aan het rad én mag u nogmaals een letter raden.  Indien je fout hebt geraden is het aan de andere speler. Klinkers kan u kopen voor €250, als je denkt het woord te weten mag je dit raden maar als je het fout hebt betaal je ook €250.
        </p>

        <router-link class="mb-2 link-as-button" :to="{ name: 'Lobby' }">Voeg je toe aan de wachtrij en speel het spel.</router-link>
        <a href="#" v-on:click="logout">Uitloggen</a>
      </div>
    </main>
  </div>
    <!--<div class="container">-->
      <!--<router-link :to="{ name: 'Lobby' }" class="btn">Play the game</router-link><hr>-->
        <!--<button class="btn-primary btn" v-on:click="logout">Logout</button>-->




    <!--</div>-->
</template>

<script>
    import * as firebase from "firebase";
    import Router from 'vue-router';
    export default {
        name: 'Profiel',
        data() {
            return {
                msg: 'Welkom ',
                displayName: '',
                password: '',
                errorCode: '',
                errorMessage: '',
                user: firebase.auth().currentUser,
//        displayName:'',
//        emailVerified:'',
//        photoURL:'',
//        isAnonymous:'',
//        uid:'',
//        providerData:'',
            }
        },
        methods: {

            getUserData: function () {
                let self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        console.log(user.displayName);
                        self.displayName = user.displayName;
                        self.msg = 'Welkom ' + self.displayName;
                    } else {
                        // User is signed out.
                        // ...
                    }
                });

            },
            logout: function () {
                let self = this
                firebase.auth().signOut().then(function () {
                    // Sign-out successful.
                    self.$router.push({name: 'Login'});

                }, function (error) {
                    // An error happened.
                });
            }

        }
        , mounted: function () {
            let self = this
            firebase.auth().onAuthStateChanged(function(user) {
                if (user) {
                    self.getUserData()
                } else {
                    self.$router.push({name: 'Lobby'});
                }
            });
        }
    }
</script>
