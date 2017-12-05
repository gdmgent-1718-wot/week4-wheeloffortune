<template>
  <div id="app" class="pt-0 mt-0">
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
