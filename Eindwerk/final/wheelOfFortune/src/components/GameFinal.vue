<template>
  <div>
    <header class="align-items container-fluid green-bg">
      <ul class='result pt-2 pl-0 small-container'>
        <li class="list-inline-item mr-1" v-for='letter in wordLetters'>
          <h3 v-if="letter == ' ' " class="text-muted" style="opacity: 0.2">
            {{ isGuessedLetter(letter) ? letter : '█'}}</h3>
          <h3 v-else class="text-uppercase">{{ isGuessedLetter(letter) ? letter : '█'}}</h3>
        </li>
      </ul>
    </header>
    <main class="container-fluid">
      <div class="small-container pt-2" style="z-index: 10000">
        <p v-for="(value, key)  in scorePlayers"><span :id="key">Score Speler {{ key }}: {{ value }} </span></p>
        <p>Gedraaide score: {{ currentScore }} </p>
        <div v-if="currentPlayer != null && currentPlayer.active" class="playing">
          <h3 class="pb-1 text-warning font-weight-bold">{{ randomWordCategory }}</h3>
          <button v-if="begin == false" class="col-12 mb-2 green-bg" style="border: none;" @click="turnWheel">Draai aan het rad!</button>
          <div v-if="begin == true">
            <h4 v-if="message" class="font-weight-bold" :style="{ color: messageColor }">{{message}}</h4>
            <button type="button" class="letter-button"
                    :disabled='single.checked || tries == 0 || showWord()' @click='handleLetterClick(single)'
                    v-for='single in alphabet'>
              {{ single.letter }}
            </button>
            <form class="pt-2">
              <label for="sel1">Koop een klinker (voor 250 euro):</label>
              <select class="form-control col-12 float-left mb-1 text-uppercase" id="sel1" v-model="vowel">
                <option class="text-uppercase" v-for="klinker in vowels" :value="klinker.id">{{ klinker.letter }}</option>
              </select>
              <button type="button" class="btn btn-primary btn col-12 mb-5 float-left" @click='unlockVowel'>
                Koop klinker. (-€250)
              </button>
            </form>
            <form class="pb-2">
              <label>Mag ik het zeggen Walter (voor 250 euro)?</label>
              <input type="text" class="col-12 form-control mb-1" placeholder="Het woord, de zin of gezegde is.."
                     @keyup.enter="didIGuessRight" v-model="walterInput">
                <button type="button" class="btn btn-primary btn col-12 mb-2 float-left"
                      @click='didIGuessRight'>Ik ga het zeggen Walter! (-€250)
              </button>
              <span v-if='walterFeedback' class="font-weight-bold mb-3">{{ walterFeedback }}</span>
            </form>
          </div>
        </div>
        <div v-else=""><p>{{ statusMessage }}</p></div>
          <video id="videoStream"></video>
      </div>
    </main>
  </div>

</template>

<script>
    import Vue from 'vue'
    import * as firebase from "firebase";
    import VueSocketio from 'vue-socket.io';
    import {throwconfetti} from '../../static/js/confetti.js';
    import Peer from 'simple-peer';
    import { bus } from '../main';

    Vue.use(VueSocketio, 'http://localhost:3000/');


    export default {
        name: 'GameFinal',
        data() {
            return {
                showStream: false,
                peer: new Peer({trickle: false}),
                msg: 'Game ',
                errorCode: '',
                errorMessage: '',
                game: null,
                user: {},
                active: false,
                answer: '',
                players: [],
                currentPlayer: null,
                currentAnswer: null,
                showText: false,
                message: '',
                begin: false,
                messageColor: 'red',
                loading: 'Willekeurig een zin, woord of gezegde kiezen...',
                words: [],
                vowel: '',
                vowels: [
                  {
                    id: 0,
                    letter: "a"
                  },
                  {
                    id: 4,
                    letter: "e"
                  },
                  {
                    id: 8,
                    letter: "i"
                  },
                  {
                    id: 14,
                    letter: "o"
                  },
                  {
                    id: 20,
                    letter: "u"
                  }
                  ],
                vowelsUsed: [],
                randomWord: '',
                randomWordCategory: '',
                compareWord: '',
                walterInput: '',
                walterFeedback: '',
                wordLetters: [],
                lettersUsed: [],
                tries: 6,
                initialTries: 6,
                alphabet: [],
                statusMessage: 'Het is momenteel aan een andere speler. Wacht uw beurt af.',
                scorePlayers: {
                 1:0,
                 2:0,
                 3:0
                },
                currentScore: '...',
                isNegative: false
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
            initializeGame() {
                this.connectToStream();
                this.tries = this.initialTries;
                this.randomWord = '';
                this.randomWordCategory = '';
                this.compareWord = '';
                this.wordLetters = [];
                this.getWord();
                this.resetCheckedLetters();
                this.lockVowels();
                this.splitWordIntoLetters();
                this.lettersUsed = [];
            },
            connectToStream(data) {
                let database = firebase.database()
                self = this;
                if (self.currentPlayer.number === data.number && !self.currentPlayer.stream) {
                    database.ref('game/players/player' + this.currentPlayer.number).update({
                        stream: true
                    });
                    self.peer.signal(data.host)
                    self.peer.on('signal', function (signal) {
                        console.log(signal);
                        self.$socket.emit('newRecievePeer', {identity: signal, number: self.currentPlayer.number});
                    })
                    self.peer.on('stream', function (stream) {
                        let video = document.querySelector('video');
                        video.src = window.URL.createObjectURL(stream);
                        video.play();

                    })
                }
            },

            turnWheel() {
              this.begin = true;
              //Neem hier de data van de camera stel nu dat het 300 is.
              this.currentScore = 300
            },

            assignScoreToPlayers () {
              let self = this
              let database = firebase.database()
              let databaseRef = database.ref('game/players');

              databaseRef.on('value', function (snapshot) {
                let playersInfo = snapshot.val()
                self.scorePlayers[1] = playersInfo.player1.score
                self.scorePlayers[2]= playersInfo.player2.score
                self.scorePlayers[3] = playersInfo.player3.score
              });
            },

            getWord() {
                this.randomWord = this.game.answer.word;
                this.randomWordCategory = 'Categorie is: ' + this.game.answer.category;
            },

            lockVowels() {
                this.alphabet[0].checked = true
                this.alphabet[4].checked = true
                this.alphabet[8].checked = true
                this.alphabet[14].checked = true
                this.alphabet[20].checked = true
            },

            unlockVowel() {
               this.substractMoneyFromCurrentMoney ();
               if(this.isNegative == false)
                  this.alphabet[this.vowel].checked = false
            },

            substractMoneyFromCurrentMoney () {
              let currentPlayerScore = this.scorePlayers[this.currentPlayer.number]
              let substractedScore = currentPlayerScore - 250
              if(substractedScore < 0){
                alert('Je score is niet hoog genoeg om een klinker te kopen of het woord te raden.')
                this.isNegative = true
              }
              else {
                this.isNegative = false
                this.scorePlayers[this.currentPlayer.number] = substractedScore
                let database = firebase.database()
                database.ref('game/players/player'+ this.currentPlayer.number).update({
                  score: substractedScore
                });
              }
//              console.log(substractedScore)
            },

            getDataFromFirebase() {
              let self = this
                let database = firebase.database()
                let databaseRef = database.ref('words');
                databaseRef.on('value', function (snapshot) {
                    self.words = snapshot.val().values
                    self.loading = 'We zoeken een zin, woord of gezegde.'
                    self.initializeGame()
                });
            },

            splitWordIntoLetters() {
                for (var i = 0; i < this.randomWord.length; i++) {
                    this.wordLetters.push(this.randomWord.toLowerCase().charAt(i));
                }
            },

            resetCheckedLetters() {
                this.alphabet.filter((single) => {
                    single.checked = false;
                });
            },

            handleLetterClick(single) {
                single.checked = true;
                let letterFromAlpha = single.letter

                let database = firebase.database()
                database.ref('game/alphabeth/').update({
                  [letterFromAlpha] : true
                });

                let letterClicked = single.letter.toLowerCase()
                this.lettersUsed.push(letterClicked);
                database.ref('game/lettersUsed').push(
                  letterClicked
                );
                this.compareWords();

                this.countItemInArray(this.wordLetters, single.letter.toLowerCase())

                if (this.wordLetters.includes(single.letter.toLowerCase())) {
                    this.messageColor = '#4BE8D8'
                    this.message = 'Je hebt juist geraden en mag nog eens draaien aan het rad.'
                    this.begin = false
                }
                else {
                    // this.messageColor = '#DD5B46'
                    // this.message = 'Helaas, deze letter zochten we niet, het is aan de volgende...'
                    this.endTurn()
                }
                this.checkIfWon()
            },

            countItemInArray(array, value) {
                let n = 0;
                for (let i = 0; i < array.length; i++) {
                    if (array[i] == value) {
                        n++
                    }
                }
                alert('je krijgt ' + n + ' keer het bedrag dat je hebt gedraait')
                this.updateScore(n)
                return n;
            },

            updateScore (times) {
              if(times != 0){
                let calculatedScore = (this.currentScore * times) + this.scorePlayers[this.currentPlayer.number]
                firebase.database().ref('game/players/player'+ this.currentPlayer.number).update({
                  score: calculatedScore
                });

                this.scorePlayers[this.currentPlayer.number] = calculatedScore
              }

              this.currentScore = '...'
            },

            isGuessedLetter(letter) {
                return this.lettersUsed.indexOf(letter.toLowerCase()) > -1;
            },

            compareWords() {
                this.compareWord = '';
                this.wordLetters.forEach((letter) => {
                    if (this.lettersUsed.indexOf(letter) > -1) {
                        this.compareWord += letter;
                    }
                });
            },

            showWord() {
                return this.randomWord == this.compareWord;
            },

            checkIfWon() {
              let wordLettersNoSpaces;
              wordLettersNoSpaces = this.wordLetters.filter(function(str) {
                return /\S/.test(str);
              })

                if (this.compareWord.length == wordLettersNoSpaces.length) {
                    this.messageColor = '#00b84f'
                    this.message = 'Proficiat! Je hebt gewonnen!!!.'
                    this.handleEndGame();
                }
            },

            didIGuessRight() {
                if (this.walterInput.replace(/\s/g, '').toLowerCase() != '' && this.walterInput.replace(/\s/g, '').toLowerCase() != null) {
                    if (this.walterInput.replace(/\s/g, '').toLowerCase() == this.randomWord.replace(/\s/g, '').toLowerCase()) {
                        this.handleEndGame();
                        this.walterFeedback = "Proficiat! U heeft het woord juist geraden!"
                    }
                    else {
                      this.substractMoneyFromCurrentMoney();
                      this.walterFeedback = "Helaas, u heeft het niet juist geraden."
                    }
                }
                else
                    this.walterFeedback = "U moet een woord invoeren.."
            },

            handleEndGame(){
              let self = this
              throwconfetti();
              clearTimeout(throwconfetti(), 5000)
              firebase.database().ref('game/lettersUsed/').set({
                0: 'a',
                1: 'b',
                2: 'c',
                3: 'd',
                4: 'e',
                5: 'f',
                6: 'g',
                7: 'h',
                8: 'i',
                9: 'j',
                10: 'k',
                11: 'l',
                12: 'm',
                13: 'n',
                14: 'o',
                15: 'p',
                16: 'q',
                17: 'r',
                18: 's',
                19: 't',
                20: 'u',
                21: 'v',
                22: 'w',
                23: 'x',
                24: 'y',
                25: 'z',
              });
              firebase.database().ref('game/finished/').update({
                end: true,
                winner: this.currentPlayer.name
              });
              setTimeout(function () {
               document.getElementById("confettiCanvas").remove();
               self.resetWholeGame();
               // self.$socket.emit('startGame')
              }, 8000)
            },

            resetWholeGame() {
              firebase.database().ref('game/players/').update({
                player1: {
                  active: true,
                  host: 0,
                  id: 1,
                  identity:0,
                  number: 1,
                  name: '',
                  playing: false,
                  score: 0,
                  stream: false,
                },
                player2: {
                  active: false,
                  host: 0,
                  id: 2,
                  identity:0,
                  number: 2,
                  name: '',
                  playing: false,
                  score: 0,
                  stream: false,
                },
                player3: {
                  active: false,
                  host: 0,
                  id: 3,
                  identity: 0,
                  number: 3,
                  name: '',
                  playing: false,
                  score: 0,
                  stream: false,
                }
              })
              firebase.database().ref('game/lettersUsed/').remove()
              firebase.database().ref('game/wasStopped/').set(false)
              this.$socket.emit('startGame')
              this.$router.push({ name: 'Profile', })
            },

            getUserData: function () {
                let self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        self.user = user;
                    }
                });
            },

            getSocketData: function () {
                let self = this;
                self.$options.sockets.turnChange = (data) => {
                    console.log(data)
                }
                self.$options.sockets.answer = (data) => {
                    self.currentAnswer = data;
                }
                self.$options.sockets.newStreamPeer = (data) => {
                    console.log('hello');
                    self.connectToStream(data);
                }
            },

            sendAnswer: function () {
                this.$socket.emit('answer', {player: this.currentPlayer.name, answer: this.answer});
                this.endTurn();
                this.answer = null;
                alert('data send')
            },

            authChange: function () {
                let self = this
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                    } else {
                        self.$router.push({name: 'Login'});
                    }
                });
            },

            getGameData: function () {
                let self = this;

                firebase.database().ref('game').on('value', function (snapshot) {
                    self.game = snapshot.val();
                    console.log('check this')
                    self.getPlayers(self.game.players)
                    self.checkArray();
                    // self.handleLettersAndVowelsUsed();
                    // self.checkIfWonAndChangeMessage();
                })
            },

            checkIfWonAndChangeMessage(){
            let self = this
            let finishedStatus;
            let playerWon;

            let finishedRef = firebase.database().ref('game/finished');
            finishedRef.on('value', function(snapshot) {
              finishedStatus = snapshot.val().end
              playerWon = snapshot.val().winner
            });

            if(finishedStatus == true){
              this.statusMessage = playerWon + ' heeft het spel gewonnen!'
              setTimeout(function () {
                self.$router.push({ name: 'Profile', })
              }, 5000)
            }
          },

            handleLettersAndVowelsUsed () {
              let self = this
              firebase.database().ref('game/lettersUsed').on('value', function (snapshot) {
                let lettersFromDatabase = snapshot.val();

                if(lettersFromDatabase != null && lettersFromDatabase.length != 0){
                  self.lettersUsed = Object.values(lettersFromDatabase)
                    self.vowelsUsed = self.lettersUsed.filter(function (obj) {
                      return obj == 'a' || obj == 'e' || obj == 'i' || obj == 'o' || obj == 'u'
                    })
                }
                else {
                  self.lettersUsed = []
                }

                for(let i = 0; i < self.vowelsUsed.length; i++){
                  self.vowels = self.vowels.filter(function (obj) {
                    return obj.letter != self.vowelsUsed[i]
                  })
                }
              })
            },

            checkArray: function () {
                this.alphabet = []
                let values = Object.values(this.game.alphabeth);
                let keys = Object.keys(this.game.alphabeth);
                if (values.length === keys.length) {
                    for (let i = 0; i < values.length; i++) {
                        this.alphabet.push({letter: keys[i], checked: values[i]})
                    }
                    //console.log(this.alphabet)
                }
            },

            getPlayers: function (players) {
                let self = this;
                self.players = [];
                self.currentPlayer = [];
                for (let player of Object.values(players)) {
                    if (player.id === self.user.uid) {
                        self.currentPlayer = player;
                        self.players.push(player)
                        let test = document.getElementById(self.currentPlayer.number)
                        test.classList.add('orange')
                    }
                    else {
                        if (player.playing) {
                            self.players.push(player);
                        }
                    }
                }
            },
            //turnbased
            endTurn: function () {
                this.$socket.emit('turnChange', {number: this.currentPlayer.number});
            },

            whenGameFinishedDatabaseChangeIsMade () {
              let self = this;
              firebase.database().ref('game/finished').on('value', function (snapshot) {
                self.checkIfWonAndChangeMessage();
              })
            },

            checkIfGameWasStopped () {
              let self = this;
              firebase.database().ref('game/wasStopped').on('value', function (snapshot) {
                if(snapshot.val() == true)
                  self.resetWholeGame()
                  // self.$socket.emit('startGame')
              })
            },
        },

      created() {
        bus.$emit('userLogin', true)
        this.authChange();
        this.getUserData();
        this.getGameData();
        this.getSocketData();
        this.getDataFromFirebase();
        this.whenGameFinishedDatabaseChangeIsMade ();
        this.handleLettersAndVowelsUsed();
        this.checkIfGameWasStopped();
        this.assignScoreToPlayers();
      },

        mounted() {
            this.authChange();
            this.getUserData();
            this.getGameData();
            this.getSocketData();
            this.getDataFromFirebase();
            this.handleLettersAndVowelsUsed();
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
</style>
