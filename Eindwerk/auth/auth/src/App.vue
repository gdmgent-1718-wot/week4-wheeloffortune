<template>
  <div id="app" class="pt-0 mt-0">
    <nav class="navbar navbar-toggleable-md navbar-light bg-faded pt-3 pb-3">
      <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <a class="navbar-brand" href="#">
        <img src="../static/img/Logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
        <span class="ml-3">Wheel of Fortune</span>
      </a>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <router-link class="nav-item nav-link active" to="/login">Login <span class="sr-only">(current)</span></router-link>
          <router-link class="nav-item nav-link" to="/admin">Add words</router-link>
          <router-link class="nav-item nav-link" to="/game">Play</router-link>
        </div>
      </div>
    </nav>
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
