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
          <button v-on:click="register" type="submit">Registreer</button>
          <router-link :to="{ name: 'Login' }">Al een account? Log je nu in.</router-link>
          <p class="error">{{message}}</p>
        </form>
      </div>
    </main>
  </div>
    <!--<div class="container">-->
        <!--<h1>{{ msg }}</h1>-->
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
            <!--<button  v-on:click="register" type="submit" class="btn btn-primary">Submit</button>-->
            <!--<router-link :to="{ name: 'Login' }">Login</router-link>-->
            <!--<p>{{message}}</p>-->
        <!--</form>-->
    <!--</div>-->
</template>

<script>
    import * as firebase from "firebase";
    import vuesocket from "vue-socket.io";

    export default {

  name: 'Register',
  data () {
    return {
      msg: 'Registreer',
        email: '',
        password:'',
        errorCode:'',
        message: '',
    }
  },
  methods: {
      register: function () {
          console.log('button is clicked');
          self = this;
          firebase.auth().createUserWithEmailAndPassword(self.email, self.password).catch(function(error) {
              // Handle Errors here.

              self.errorCode = error.code;
              self.message = error.message;
              console.log(error)


          }).then(function() {
              firebase.auth().onAuthStateChanged(function(user) {
                  if (user) {
                      console.log('registered')
                      self.message = "successfully registered"
                      self.$router.push({name: 'Completion'});
                  } else {
                      // No user is signed in.
                  }
              });

          });

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
