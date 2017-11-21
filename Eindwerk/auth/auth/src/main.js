// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import * as firebase from "firebase";


var config = {
    apiKey: "AIzaSyCRDbOBN_g2rlAqy8NBSRmjfvrPMswf4EE",
    authDomain: "wheeloffortune2-c0e4a.firebaseapp.com",
    databaseURL: "https://wheeloffortune2-c0e4a.firebaseio.com/",
    storageBucket: "gs://wheeloffortune2-c0e4a.appspot.com/",
};
firebase.initializeApp(config);

Vue.config.productionTip = false
require('../node_modules/bootstrap-sass/assets/stylesheets/_bootstrap.scss')
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
