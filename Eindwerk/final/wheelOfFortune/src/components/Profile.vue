<template>
    <div class="container">
        <h1>{{ msg }}</h1>
        <button v-on:click="logout">logout</button>
        <router-link :to="{ name: 'Lobby' }">Play the game</router-link>



    </div>
</template>

<script>
    import * as firebase from "firebase";
    import Router from 'vue-router';
    export default {
        name: 'Profile',
        data() {
            return {
                msg: 'Welcome ',
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
                        self.msg = 'Welcome ' + self.displayName;
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
