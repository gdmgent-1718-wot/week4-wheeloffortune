<template>
  <div>
    <header class="align-items container-fluid red-bg">
      <div class="align-center">
        <h1>{{ msg }}</h1>
      </div>
    </header>
    <main class="container-fluid">
      <div class="small-container pt-5">
        <form class="col-12">
          <label for="emailid">Email</label>
          <input v-model="email" class="col-10" type="text"  id="emailid" aria-describedby="emailHelp" placeholder="janmodaal@test.be">
          <label for="passwordid">Wachtwoord</label>
          <input v-model="password" id="passwordid" placeholder="Password" class="col-10" type="password">
          <button v-on:click="login" type="submit">Log in</button>
          <router-link :to="{ name: 'Register' }">Nog geen account? Registreer nu.</router-link>
          <p class="error">{{errorMessage}}</p>
        </form>
      </div>
    </main>
  </div>
    <!--<main class="container mt-5" >-->
            <!--<h1</h1>-->
            <!--<form>-->
                <!--<div class="form-group">-->
                    <!--<label for="emailid">Email address</label>-->
                    <!--<input v-model="email" type="email" class="form-control" id="emailid" aria-describedby="emailHelp" placeholder="Enter email">-->
                    <!--<small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>-->
                <!--</div>-->
                <!--<div class="form-group">-->
                    <!--<label for="passwordid">Password</label>-->
                    <!--<input v-model="password" type="password" class="form-control" id="passwordid" placeholder="Password">-->
                <!--</div>-->
                <!--<button  v-on:click="login" type="submit" class="btn btn-primary">Submit</button><hr>-->
                <!--<router-link :to="{ name: 'Register' }">Register</router-link>-->
                <!--<p>{{errorMessage}}</p>-->
            <!--</form>-->
    <!--</main>-->
</template>

<script>
    import * as firebase from "firebase";
    import Router from 'vue-router';
    import vuesocket from "vue-socket.io";
    import { bus } from '../main';


    export default {
  name: 'Login',
  data () {
    return {
      msg: 'Login',
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
                        bus.$emit('userLogin', true)
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
