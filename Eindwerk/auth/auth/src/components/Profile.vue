<template>
    <div class="container">
        <h1>{{ msg }}</h1>
        <button v-on:click="logout">logout</button>

    </div>
</template>

<script>
    import * as firebase from "firebase";
    import Router from 'vue-router';
    export default {
        name: 'Profile',
        data() {
            return {
                msg: 'Welcome',
                email: '',
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
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        console.log(user);
                    } else {
                        // User is signed out.
                        // ...
                    }
                });

            },
            logout: function () {
                self = this
                firebase.auth().signOut().then(function () {
                    // Sign-out successful.
                    self.$router.push({name: 'Login'});

                }, function (error) {
                    // An error happened.
                });
            }

        }
        , mounted: function () {
            if (!this.user) {
                this.$router.push({name: 'Login'});
            }
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
