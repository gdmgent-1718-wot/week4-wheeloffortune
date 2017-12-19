<template>
    <main class="container mt-5" >
            <h1>{{ msg }}</h1>
            <form>
                <div class="form-group">
                    <label for="emailid">Email address</label>
                    <input v-model="email" type="email" class="form-control" id="emailid" aria-describedby="emailHelp" placeholder="Enter email">
                    <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
                </div>
                <div class="form-group">
                    <label for="passwordid">Password</label>
                    <input v-model="password" type="password" class="form-control" id="passwordid" placeholder="Password">
                </div>
                <button  v-on:click="login" type="submit" class="btn btn-primary">Submit</button><hr>
                <router-link :to="{ name: 'Register' }">Register</router-link>
                <p>{{errorMessage}}</p>
            </form>
    </main>
</template>

<script>
    import * as firebase from "firebase";
    import Router from 'vue-router';
    import vuesocket from "vue-socket.io";


    export default {
  name: 'Login',
  data () {
    return {
      msg: 'Login test',
        email: '',
        password:'',
        errorCode:'',
        errorMessage: '',
        user: firebase.auth().currentUser,

    }
  },
    methods: {
        login: function () {
            let self = this;
            console.log(self.user);
            firebase.auth().signInWithEmailAndPassword(self.email, self.password).catch(function(error) {
                // Handle Errors here.
                self.errorCode = error.code;
                self.errorMessage = error.message;
            }).then(function () {
                firebase.auth().onAuthStateChanged(function(user) {
                    if (user) {
                        self.$router.push({name: 'Profile'});
                    } else {
                        // No user is signed in.
                    }
                });
            });

        }
    }
    ,created: function () {
            console.log('test');
            if(this.user){
                this.$router.push({name: 'Profile'});
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
