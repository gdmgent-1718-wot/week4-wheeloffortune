<template>
    <div class="container">
        <h1>{{ msg }}</h1>
        <form>
            <div class="form-group">
                <label for="exampleInputEmail1">Email address</label>
                <input v-model="email" type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email">
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <div class="form-group">
                <label for="exampleInputPassword1">Password</label>
                <input v-model="password" type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
            </div>
            <button  v-on:click="register" type="submit" class="btn btn-primary">Submit</button>
            <router-link :to="{ name: 'Login' }">Login</router-link>
            <p>{{errorMessage}}</p>
        </form>
    </div>
</template>

<script>
    import * as firebase from "firebase";
    export default {

  name: 'Register',
  data () {
    return {
      msg: 'Register for a new account',
        email: '',
        password:'',
        errorCode:'',
        errorMessage: '',
    }
  },
  methods: {
      register: function () {
          self = this;
          firebase.auth().createUserWithEmailAndPassword(self.email, self.password).catch(function(error) {
              // Handle Errors here.
              self.errorCode = error.code;
              self.errorMessage = error.message;
              console.log('registerd')
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
