<template>
    <main class="container mt-5">
        <div class="col-lg-6 offset-lg-3">
            <div class="pb-5">
                <h1 class="text-warning">{{ loading }}</h1>
                <ul class='result pt-2 pl-0'>
                    <li class="list-inline-item mr-1" v-for='letter in wordLetters'>
                        <h1 v-if="letter == ' ' " class="text-muted" style="opacity: 0.2">
                            {{ isGuessedLetter(letter) ? letter : '█'}}</h1>
                        <h1 v-else class="text-warning text-uppercase">{{ isGuessedLetter(letter) ? letter : '█'}}</h1>
                    </li>
                </ul>

            </div>
            <div v-if="currentPlayer.active" class="playing">
                <h5 class="pb-1 text-warning font-weight-bold">{{ randomWordCategory }}</h5>
                <p class="pb-1 text-muted">De grijze vakjes zijn spaties.</p>
                <h4 class="pb-3 pt-1 font-weight-bold" :style="{ color: messageColor }">{{message}}</h4>
                <button type="button" class="btn btn-secondary col-2"
                        :disabled='single.checked || tries == 0 || showWord()' @click='handleLetterClick(single)'
                        v-for='single in alphabet'>
                    {{ single.letter }}
                </button>
                <form>
                    <div class="form-group">
                        <label for="sel1">Koop een klinker (voor 250 euro):</label>
                        <select class="form-control col-12 float-left mb-1" id="sel1" v-model="vowel">
                            <option value="0">A</option>
                            <option value="4">E</option>
                            <option value="8">I</option>
                            <option value="14">O</option>
                            <option value="20">U</option>
                        </select>
                        <button type="button" class="btn btn-primary btn col-12 mb-5 float-left" @click='unlockVowel'>
                            Bevestig
                        </button>
                    </div>
                </form>
                <form>
                    <div class="form-group">
                        <label>Mag ik het zeggen Walter (voor 250)?</label>
                        <div class="col-12 float-left p-0">
                            <input type="text" class="form-control mb-1" placeholder="Het woord, de zin of gezegde is.."
                                   @keyup.enter="didIGuessRight" v-model="walterInput">
                        </div>
                        <button type="button" class="btn btn-primary btn col-12 mb-2 float-left"
                                @click='didIGuessRight'>Ik ga het zeggen Walter!
                        </button>
                    </div>
                    <span v-if='walterFeedback' class="font-weight-bold mb-3">{{ walterFeedback }}</span>
                </form>
            </div>
            <div v-else=""


            <div class="pb-2 pt-5 mt-5 text-muted">
                Raad een letter uit een zin, woord of gezegde, als u het <span class="text-success font-weight-bold">juist</span>
                heeft mag u <span class="text-success font-weight-bold">nog eens draaien</span>
                aan het rad én mag u nogmaals een letter raden.
                Indien je <span class="text-danger font-weight-bold">fout</span> hebt geraden is het aan de <span
                    class="text-danger font-weight-bold">andere speler</span>.
            </div>
        </div>
    </main>
</template>

<script>
    import Vue from 'vue'
    import * as firebase from "firebase";
    import VueSocketio from 'vue-socket.io';

    Vue.use(VueSocketio, 'http://localhost:3000/');


    export default {
        name: 'GameFinal',
        data() {
            return {
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
                messageColor: 'red',
                loading: 'Willekeurig een zin, woord of gezegde kiezen...',
                words: [],
                vowel: '',
                randomWord: '',
                randomWordCategory: '',
                compareWord: '',
                walterInput: '',
                walterFeedback: '',
                wordLetters: [],
                lettersUsed: [],
                tries: 6,
                initialTries: 6,
                alphabet: []
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
                //this.alphabet = [];
                this.tries = this.initialTries;
                this.randomWord = '';
                this.randomWordCategory = '';
                this.compareWord = '';
                this.wordLetters = [];
                this.lettersUsed = [];
//                this.asignRandomWordToFirebase();
                this.getWord();
                this.resetCheckedLetters();
                this.lockVowels();
                this.splitWordIntoLetters();
            },

//            asignRandomWordToFirebase () {
//              let randomNumber = Math.floor(Math.random() * this.words.length);
//              let randomWordForFirebase = this.words[randomNumber][0];
//              let randomWordCategoryForFirebase = 'Categorie is: ' + this.words[randomNumber][1];
//              let database = firebase.database()
//              database.ref('game/answer').update({
//                category: randomWordCategoryForFirebase,
//                word: randomWordForFirebase,
//              });
//            },

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
                this.alphabet[this.vowel].checked = false
            },

            getDataFromFirebase() {
              self = this
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

                this.lettersUsed.push(single.letter.toLowerCase());
                this.compareWords();

                this.countItemInArray(this.wordLetters, single.letter.toLowerCase())

                if (this.wordLetters.includes(single.letter.toLowerCase())) {
                    this.messageColor = '#5cb85c'
                    this.message = 'Je hebt juist geraden en mag nog eens draaien aan het rad.'
                }
                else {
                    this.messageColor = '#d9534f'
                    this.message = 'Helaas, deze letter zochten we niet, het is aan de volgende...'
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
                return n;
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
                if (this.compareWord.length == this.wordLetters.length) {
                    this.messageColor = '#00b84f'
                    this.message = 'Proficiat! Je hebt gewonnen!!!.'
                }
            },

            didIGuessRight() {
                if (this.walterInput.replace(/\s/g, '').toLowerCase() != '' && this.walterInput.replace(/\s/g, '').toLowerCase() != null) {
                    if (this.walterInput.replace(/\s/g, '').toLowerCase() == this.randomWord.replace(/\s/g, '').toLowerCase()) {
                        this.walterFeedback = "Proficiat! U heeft het woord juist geraden!"
                    }
                    else
                        this.walterFeedback = "Helaas, u heeft het niet juist geraden."
                }
                else
                    this.walterFeedback = "U moet een woord invoeren.."
            },
            getUserData: function () {
                self = this;
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                        self.user = user;
                    }
                });
            },
            getSocketData: function () {
                self = this;
                self.$options.sockets.turnChange = (data) => {
                    console.log(data)
                }
                self.$options.sockets.answer = (data) => {
                    self.currentAnswer = data;
                }
            },
            sendAnswer: function () {
                this.$socket.emit('answer', {player: this.currentPlayer.name, answer: this.answer});
                this.endTurn();
                this.answer = null;
            },
            authChange: function () {
                self = this
                firebase.auth().onAuthStateChanged(function (user) {
                    if (user) {
                    } else {
                        self.$router.push({name: 'Login'});
                    }
                });
            },
            getGameData: function () {
                self = this;

                firebase.database().ref('game').on('value', function (snapshot) {
                    console.log(snapshot.val());
                    self.game = snapshot.val();
                    self.getPlayers(self.game.players)
                    self.checkArray();
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
                    console.log(this.alphabet)
                }
            },
            getPlayers: function (players) {
                self = this;
                self.players = [];
                self.currentPlayer = [];
                for (let player of Object.values(players)) {

                    if (player.id === self.user.uid) {
                        self.currentPlayer = player;
                        self.players.push(player)
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
        },
        mounted() {
            this.authChange();
            this.getUserData();
            this.getGameData();
            this.getSocketData();
            this.getDataFromFirebase();
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
