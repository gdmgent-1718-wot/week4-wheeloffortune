<template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>

<script>
    export default {
  name: 'app',
        data () {
            return {
                msg: 'Login test',
                email: '',
                password:'',
                errorCode:'',
                errorMessage: '',
                displayName:'',
                emailVerified:'',
                photoURL:'',
                isAnonymous:'',
                uid:'',
                providerData:'',
            }
        }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
