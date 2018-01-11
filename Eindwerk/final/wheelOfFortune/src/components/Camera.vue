<template>
  <div>
    <video autoplay></video>
    <br>
    <canvas id="video"></canvas>
    <canvas style="position: absolute" id="overlay"></canvas>
    <div>
      <p>{{ rgb }}</p>
      <p v-if="color">De kleur dat ik zie is: {{ color }}</p>
      <p v-if="score">De speler maakt kans om {{ score }} euro te winnen.</p>
      <label title="X position">X position</label>
      <input type="range" min="0" max="640" @change="setPixel" name="X position" v-model="x"/>
      <label title="Y position">Y position</label>
      <input type="range" min="0" max="480" @change="setPixel" name="Y position" v-model="y"/>
    </div>
  </div>
</template>

<script>
// Import dependencies.
import Vue from "vue";
import * as firebase from "firebase";
import Peer from "simple-peer";
import VueSocketio from "vue-socket.io";

Vue.use(VueSocketio, "http://localhost:5000/");
// When building:
// Vue.use(VueSocketio, 'https://wheeloffortune1718.herokuapp.com/');

export default {
  name: "Camera",
  data() {
    return {
      video: null,
      constraints: { audio: false, video: true },
      database: firebase.database(),
      parameters: {
        trickle: false,
        initiator: true,
        stream: null
      },
      peers: [],
      firebaseObject: null,
      players: null,
      canvas: null,
      overlay: null,
      ctx: null,
      octx: null,
      x: 100,
      y: 100,
      videoWidth: null,
      videoHeight: null,
      rgb: [],
      rgbFormatted: "",
      color: '',
      score: ''
    };
  },
  // Make a connection with Sockets, you can recieve triggers.
  sockets: {
    connect: function() {
      console.log("Socket succesfuly connected.");
    },
    customEmit: function(val) {
      console.log(
        'This method was fired by the socket server. eg: io.emit("customEmit", data)'
      );
    }
  },
  methods: {
    // Connect with sockets to recieve data.
    getSockets: function() {
      let self = this;
      self.$options.sockets.newRecievePeer = data => {
        // Get peer info.
        console.log(self.peers[data.number - 1]);
        self.peers[data.number - 1].signal(data.identity);
      };
      self.$options.sockets.letMeWatch = data => {
        // Recieve connection requests to livestream.
        console.log("Some requests to watch Wheel of Fortune.");
        self.newPlayerStream(data);
      };
      self.$options.sockets.acceptConnection = data => {
        // Allow connection requests to livestream.
        console.log("Allow the request so they can watch Wheel of Fortune.");
        console.log(self.parameters);
        //                    self.startStream(data);
        self.peers[data.peerIndex].signal(data.playerSignal);
        //                    self.$socket.emit('startStream', data);
      };

      // Ask the color
      self.$options.sockets.getScore = data => {
        // Get the score.
        self.getPixelColor();
      };
    },
    // New stream openened for a player.
    newPlayerStream(data) {
      let self = this;
      let peer = new Peer(self.parameters);
      self.peers.push(peer);
      let index = 0;
      if (self.peers.length >= 1) {
        index = self.peers.length - 1;
      }
      console.log(self.peers);
      peer.on("signal", function(signal) {
        console.log(signal);
        self.$socket.emit("startConnection", {
          playerNum: data.playerNum,
          hostSignal: JSON.stringify(signal),
          peerIndex: index
        });
      });
    },
    // Start the stream.
    startStream(data) {},
    // Draw an overlay on top of canvas. Not being used.
    // initializeOverlay: function() {},

    // Make a canvas.
    initializeCanvas: function() {
      let self = this;
      // Make a canvas where the video will be shown.
      let canvas = document.querySelector("canvas");
      let overlay = document.getElementById("overlay");
      // Canvascontext.
      self.ctx = canvas.getContext("2d");
      // Overlay context.
      self.octx = overlay.getContext("2d");
      let video = self.video;
      // Let the video play.
      video.addEventListener(
        "play",
        function() {
          self.videoHeight = this.videoHeight;
          self.videoWidth = this.videoWidth;
          canvas.width = self.videoWidth;
          canvas.height = self.videoHeight;
          overlay.width = self.videoWidth;
          overlay.height = self.videoHeight;
          overlay.style.position = "absolute";
          overlay.style.left = 0;
          //                    video.style.display = "none";
          self.canvas = canvas;
          self.overlay = overlay;
          let $this = this; //cache

          (function loop() {
            if (!$this.paused && !$this.ended) {
              self.ctx.drawImage($this, 0, 0);
              setTimeout(loop, 1000 / 30); // drawing at 30fps
            }
          })();
          self.getPixelColor();
          self.setPixel();
        },
        0
      );
    },
    getPixelColor: function() {
      let self = this;
      // Get info from the Canvascontext.
      let pixel = self.ctx.getImageData(self.x, self.y, 1, 1);
      // This info will be a Uint8ClampedArray representing RGBA but everything will be between 0-255.
      let pixeldata = pixel.data;
      // Write RGB values to array.
      self.rgb = [pixeldata[0], pixeldata[1], pixeldata[2]];
      // Convert the pixel data to RBGa object.
      self.rgbFormatted =
        "rgb(" + pixeldata[0] + ", " + pixeldata[1] + ", " + pixeldata[2] + ")";

      // Check the color and assign a score.
      self.checkWhichColorWithRange(pixeldata[0], pixeldata[1], pixeldata[2]);

      // Give score to server.
      self.$socket.emit("giveScore", self.score);
    },
    // Place red pixel on overlay where you want, will set x and y coordinates.
    setPixel: function() {
      let self = this;
      self.octx.clearRect(0, 0, self.videoWidth, self.videoHeight);

      self.octx.fillStyle = "rgba(0, 0, 0, 0.75)";
      self.octx.fillRect(0, 0, self.videoWidth, self.videoHeight);
      self.octx.fillStyle = "#f00";
      self.octx.fillRect(self.x, self.y, 5, 5);
      self.getPixelColor();
      console.log("setting pixel");
    },
    //
    getVideo: function() {
      let self = this;
      navigator.getUserMedia =
        navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia;
      self.video = document.querySelector("video");

      navigator.getUserMedia(
        this.constraints,
        function(stream) {
          self.video.src = window.URL.createObjectURL(stream);
          self.parameters.stream = stream;
          self.initializeCanvas();
        },
        function(error) {
          console.log("getUserMedia error: ", error);
        }
      );
    },
    // Check the range of the color detected, if it is between .. and .. it corresponds to Score ...
    checkWhichColorWithRange(pixelRed, pixelGreen,pixelBlue) {
      // Check of het blauw is?
      if(this.colorDistance(78,163,255, pixelRed, pixelGreen, pixelBlue) == true){
        this.color = 'blauw!'
        this.score = 100
      }
      if(this.colorDistance(93, 115, 74, pixelRed, pixelGreen, pixelBlue) == true){
        this.color = 'groen!'
        this.score = 50
      }
      if(this.colorDistance(250, 230, 78, pixelRed, pixelGreen, pixelBlue) == true){
        this.color = 'geel!'
        this.score = 150
      }
      if(this.colorDistance(24, 19, 11 , pixelRed, pixelGreen, pixelBlue) == true){
        this.color = 'zwart!'
        this.score = 0
      }
      if(this.colorDistance(60, 47, 104 , pixelRed, pixelGreen, pixelBlue) == true){
        this.color = 'paars!'
        this.score = 50
      }
      if(this.colorDistance(176, 63, 9, pixelRed, pixelGreen, pixelBlue) == true){
        this.color = 'rood!'
        this.score = 50
      }
      if(this.colorDistance(175, 77, 4, pixelRed, pixelGreen, pixelBlue) == true){
        this.color = 'oranje!'
        this.score = 250
      }
      if(this.colorDistance(166, 53, 58, pixelRed, pixelGreen, pixelBlue) == true){
        this.color = 'roze!'
        this.score = 25
      }
    },

    colorDistance(colorRed, colorGreen, colorBlue, pixelRed, pixelGreen, pixelBlue ) {
      let diffR, diffG, diffB;

      // distance to color
      diffR = colorRed - pixelRed;
      diffG = colorGreen - pixelGreen;
      diffB = colorBlue - pixelBlue;

      let difference = Math.sqrt(diffR * diffR + diffG * diffG + diffB * diffB);
      console.log(difference)
      if(difference < 98){
        return true
      }
      else {
        return false
      }
    }
  },
  mounted() {
    this.getVideo();
    this.getSockets();
  }
};
</script>
