<template>
    <div class="parent">
        <nav class="navbar navbar-toggleable-md navbar-light bg-faded pt-3 pb-3">
            <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href="#">
                <img src="img/Logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
                <span class="ml-3">Wheel of Fortune</span>
            </a>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <a class="nav-item nav-link active" href="#">Login <span class="sr-only">(current)</span></a>
                    <a class="nav-item nav-link" href="admin.html">Add words</a>
                    <a class="nav-item nav-link" href="index.html">Play</a>
                </div>
            </div>
        </nav>
        <div id="app">
            <router-view/>
        </div>
    </div>
</template>

<script>
export default {
  name: 'app'
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
