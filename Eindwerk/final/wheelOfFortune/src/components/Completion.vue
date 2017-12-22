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
          <label for="displaynameid">Username</label>
          <input v-model="displayName" type="text" class="form-control" id="displaynameid" aria-describedby="emailHelp" placeholder="Enter email">
          <label for="phoneid">Phone number</label>
          <input v-model="phoneNumber" type="tel" class="form-control" id="phoneid" placeholder="phone number">
          <label for="emailid">Email</label>
          <input v-model="email" type="email" class="form-control" id="emailid" placeholder="email">
          <button  v-on:click="updateUserData" type="submit" class="btn btn-primary">Update</button>
          <p>{{errorMessage}}</p>
        </form>
      </div>
    </main>
  </div>
    <!--<div class="container">-->
        <!--<h1>{{ msg }}</h1>-->
        <!--<form>-->
            <!--<div class="form-group">-->
                <!--<label for="displaynameid">Username</label>-->
                <!--<input v-model="displayName" type="text" class="form-control" id="displaynameid" aria-describedby="emailHelp" placeholder="Enter email">-->
            <!--</div>-->
            <!--<div class="form-group">-->
                <!--<label for="phoneid">Phone number</label>-->
                <!--<input v-model="phoneNumber" type="tel" class="form-control" id="phoneid" placeholder="phone number">-->
            <!--</div>-->
            <!--<div class="form-group">-->
                <!--<label for="emailid">Email</label>-->
                <!--<input v-model="email" type="email" class="form-control" id="emailid" placeholder="email">-->
            <!--</div>-->
            <!--<button  v-on:click="updateUserData" type="submit" class="btn btn-primary">Update</button>-->
            <!--<p>{{errorMessage}}</p>-->
        <!--</form>-->
    <!--</div>-->
</template>

<script>
    import * as firebase from "firebase";
    import Router from 'vue-router';
    export default {
        name: 'Completion',
        data() {
            return {
                msg: 'Complete your profile',
                displayName: '',
                phoneNumber: '',
                imageURL: 'http://hope4merton.com/wp-content/uploads/2015/12/profile-placeholder.gif',
                email: '',
                errorCode: '',
                errorMessage: '',
                user:'',
            }
        },
        methods: {
            getUserData: function () {
                self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        console.log(user);
                        self.user = user;
                        self.displayName = user.displayName;
                        self.email = user.email;
                        self.imageURL = user.photoURL;
                    }
                });
            },
            updateUserData: function () {
                //todo upload profile picture
                self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        console.log(user)
                        user.updateProfile({
                            displayName: self.displayName,
                            photoURL: self.imageURL,
                            email: self.email
                        }).then(function() {
                            // Update successful.
                            self.$router.push({name: 'Profile'});
                        }).catch(function(error) {
                            self.errorMessage = error.message;
                        });
                    }
                });
//                user = firebase.auth().currentUser;
//                console.log(user);

            }

        }
        , mounted: function () {
            self = this;
            self.getUserData();
            firebase.auth().onAuthStateChanged(function(user) {
                if (user) {
                } else {
                    self.$router.push({name: 'Login'});
                }
            });
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
