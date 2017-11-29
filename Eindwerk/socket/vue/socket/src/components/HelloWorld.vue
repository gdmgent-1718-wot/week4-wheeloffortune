<template>
    <div class="hello">
        <h1>{{ msg }}</h1>
        <button v-on:click="clickButton">test</button>
    </div>
</template>

<script>
    export default {
        name: 'HelloWorld',
        data() {
            return {
                msg: 'Welcome to Your Vue.js App'
            }
        },
        sockets: {
            connect: function () {
                console.log('socket connected')
            },
            customEmit: function (val) {
                console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)')
            }
        },
        methods: {
            clickButton: function(val){
                console.log('clicked');
                // $socket is socket.io-client instance
                this.$socket.emit('chatMessage', {message: "test", name: "bob" } );
            }
        },
        mounted: function () {
            console.log('getting data')
            this.$options.sockets.chatMessage= (data) => {
                console.log(data)
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
