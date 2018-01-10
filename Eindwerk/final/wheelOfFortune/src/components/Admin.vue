<template>
  <div>
    <header class="align-items container-fluid lightgreen-bg">
      <div class="align-center">
        <h1>Admin</h1>
      </div>
    </header>
    <main class="container-fluid">
      <div class="small-container pt-5">
        <form class="col-12">
          <input type="text" @keyup.enter="addWordToArray" class="col-12 form-control" placeholder="Voeg een woord toe dat de spelers moeten raden.." aria-label="Voeg een woord toe.." v-model="inputWord">
          <select class="col-12 form-control mb-3" v-model="selected">
            <option value="" selected disabled hidden>Selecteer een categorie</option>
            <option v-for="category in categories" :value="category">
              {{ category.name }}
            </option>
          </select>
          <span class="input-group-btn">
              <button class="col-12 btn btn-secondary bg-success lightgreen-bg" style="border: none" type="button" @click="addWordToArray">
                  Voeg het toe aan de lijst, vergeet niet op te slaan.
              </button>
          </span>
        </form>
        <div class="form-group mt-3">
          <span class="description text-muted"><em>{{ selected.description }}</em></span>
        </div>
        <h4 class="pt-5 pb-2">Te raden zinnen, woorden of gezegdes:</h4>
        <button class="col-md-6 col-sm-12 mb-2 btn btn-secondary"  type="button" @click="pushDataToFirebase(arrayOfWords)" :class="{'btn-danger': isRed, 'btn-success': isGreen}">
          {{ buttonText }}
        </button>
        <div style="overflow-x: auto">
          <table class="table col-12">
            <thead>
            <tr>
              <th>Zin, woord of gezegde</th>
              <th>Categorie</th>
              <th>Delete</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="word in arrayOfWords" :key="word.id">
              <td class="text-left">{{ word[0] }}</td>
              <td class="text-left">{{ word[1] }}</td>
              <td>
                <button type="button" style="border: none" class="red-bg btn btn-sm btn-danger" @click="removeWordFromArray(word)">X</button> </td>
            </tr>
            </tbody>
          </table>
        </div>
        <button class="col-md-6 col-sm-12 mb-5 btn btn-secondary"  type="button" @click="pushDataToFirebase(arrayOfWords)" :class="{'btn-danger': isRed, 'btn-success': isGreen}">
          {{ buttonText }}
        </button>
      </div>
    </main>
  </div>
</template>

<script>
import Vue from "vue";
import * as firebase from "firebase";
import { bus } from "../main";
import VueSocketio from "vue-socket.io";

Vue.use(VueSocketio, "http://localhost:3000/");

export default {
  name: "Lobby",
  data() {
    return {
      inputWord: "",
      input: [],
      arrayOfWords: [],
      id: null,
      isGreen: false,
      isRed: false,
      buttonText: "Vergeet niet op te slaan!",
      description: "Selecteer een categorie",
      selected: "",
      categories: []
    };
  },
  methods: {
    changeDescription() {
      this.description = this.selected.description;
    },
    addWordToArray() {
      if (
        this.selected.description == "" ||
        this.selected.description == "U moet een categorie selecteren!"
      ) {
        this.selected.description = "U moet een categorie selecteren!";
      } else {
        this.input.push(this.inputWord);
        this.input.push(this.selected.name);
        this.arrayOfWords.unshift(this.input);
        this.input = "";
        this.inputWord = "";
        this.makeButtonRed();
      }
    },
    removeWordFromArray(word) {
      this.arrayOfWords.splice(this.arrayOfWords.indexOf(word), 1);
      this.makeButtonRed();
    },
    pushDataToFirebase(words) {
      let database = firebase.database();
      database.ref("words").set({
        values: words
      });
      this.makeButtonGreen();
    },
    getDataFromFirebase() {
      this.makeButtonGreen();
      let self = this;
      let database = firebase.database();
      let databaseRef = database.ref("words");
      let databaseRefCat = database.ref("categories");
      console.log(databaseRefCat);
      databaseRef.on("value", function(snapshot) {
        self.arrayOfWords = snapshot.val().values;
        //                    console.log(self.arrayOfWords)
      });
      databaseRefCat.on("value", function(catSnapshot) {
        self.categories = catSnapshot.val();
        console.log("teeeeeeeeeeeeeest", self.categories);
      });
    },
    makeButtonGreen() {
      this.isRed = false;
      this.isGreen = true;
      this.buttonText = "Wijzigingen opgeslagen!";
    },
    makeButtonRed() {
      this.isGreen = false;
      this.isRed = true;
      this.buttonText = "Klik hier om wijzigingen op te slaan!";
    }
  },

  mounted: function() {
    bus.$emit("userLogin", true);
    this.getDataFromFirebase();
  }
};
</script>
