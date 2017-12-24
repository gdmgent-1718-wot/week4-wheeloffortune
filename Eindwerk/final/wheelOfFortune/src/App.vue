<template>
    <div class="parent">
        <!--<nav class="navbar navbar-toggleable-md navbar-light bg-faded pt-3 pb-3">-->
            <!--<button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">-->
                <!--<span class="navbar-toggler-icon"></span>-->
            <!--</button>-->
            <!--<router-link class="navbar-brand" to="profile">-->
                <!--<img src="static/img/Logo.png" width="30" height="30" class="d-inline-block align-top" alt="">-->
                <!--<span class="ml-3">Wheel of Fortune</span>-->
            <!--</router-link>-->
            <!--<div class="collapse navbar-collapse" id="navbarNavAltMarkup">-->
                <!--<div class="navbar-nav">-->
                    <!--<router-link class="nav-item nav-link active" to="/">Login <span class="sr-only">(current)</span></router-link>-->
                    <!--<router-link class="nav-item nav-link" to="game">Play</router-link>-->
                    <!--<router-link to="profile" class="nav-item nav-link">Profile</router-link>-->
                    <!--<router-link to="admin" class="nav-item nav-link">Admin</router-link>-->
                <!--</div>-->
            <!--</div>-->
        <!--</nav>-->
      <div id="myNav" class="overlay">
        <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
        <div class="overlay-content">
          <h3 v-if="loggedIn == false"><router-link onclick="closeNav()" class="nav-item nav-link active" to="/">Login</router-link></h3>
          <h3 v-if="loggedIn"><router-link onclick="closeNav()" class="nav-item nav-link active" to="/">Logout</router-link></h3>
          <h3><router-link onclick="closeNav()" class="nav-item nav-link" to="game">Play</router-link></h3>
          <h3><router-link onclick="closeNav()" to="profile" class="nav-item nav-link">Profile</router-link></h3>
          <h3><router-link onclick="closeNav()" to="admin" class="nav-item nav-link">Admin</router-link></h3>
        </div>
      </div>
      <nav class="container-fluid red-bg">
        <img src="../static/img/logo.png" class="logo">
        <a href="#"><img src="../static/img/menu.png" class="menu-icon" onclick="openNav()"></a>
      </nav>
        <div id="app">
            <router-view/>
        </div>
    </div>
</template>

<script>
  import { bus } from './main';
  import * as firebase from "firebase";

export default {
  name: 'app',
  data () {
    return {
      user: firebase.auth().currentUser,
      loggedIn: false,
    }
  },
  created () {
    let self = this
    bus.$on('userLogin', () => {
      self.checkIfOnline();
    })
  },
  methods: {
    checkIfOnline (){
      let self = this
      console.log('teeeeeeest',self.loggedIn)
      firebase.auth().onAuthStateChanged(function (user) {
        if(user != undefined){
          self.loggedIn = true
          console.log(self.loggedIn)
        }
        else {
          self.loggedIn = false
          console.log(self.loggedIn)
        }
      }
      )}
    }
  }
</script>
