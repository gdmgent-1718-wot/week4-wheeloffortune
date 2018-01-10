<template>
    <div>
        <video autoplay></video>
        <br>
        <canvas id="video"></canvas>
        <canvas style="position: absolute" id="overlay"></canvas>
        <div>
            <label title="X position">X position</label>
            <input type="range" min="0" max="640" @change="setPixel" name="X position" v-model="x"/>
            <label title="Y position">Y position</label>
            <input type="range" min="0" max="480" @change="setPixel" name="Y position" v-model="y"/>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import * as firebase from "firebase";
import Peer from "simple-peer";
import VueSocketio from "vue-socket.io";

Vue.use(VueSocketio, "http://localhost:3000/");

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
      peers: null,
      firebaseObject: null,
      players: null,
      canvas: null,
      overlay: null,
      ctx: null,
      octx: null,
      x: 100,
      y: 100,
      videoWidth: null,
      videoHeight: null
    };
  },
  sockets: {
    connect: function() {
      console.log("socket connected");
    },
    customEmit: function(val) {
      console.log(
        'this method was fired by the socket server. eg: io.emit("customEmit", data)'
      );
    }
  },
  methods: {
    getSockets: function() {
      console.log("test");
      self = this;
      self.$options.sockets.newRecievePeer = data => {
        console.log("fuck ruck");
        console.log(self.peers[data.number - 1]);
        self.peers[data.number - 1].signal(data.identity);
      };
      self.$options.sockets.getColor = data => {
        console.log(data);
        self.peers[data.number - 1].signal(data.identity);
      };
    },
    initializeOverlay: function() {},
    initializeCanvas: function() {
      self = this;
      let canvas = document.querySelector("canvas");
      let overlay = document.getElementById("overlay");
      self.ctx = canvas.getContext("2d");
      self.octx = overlay.getContext("2d");
      let video = self.video;

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
      self = this;
      let pixel = self.ctx.getImageData(self.x, self.y, 1, 1);
      console.log(pixel.data);
    },
    setPixel: function() {
      self = this;
      self.octx.clearRect(0, 0, self.videoWidth, self.videoHeight);

      self.octx.fillStyle = "rgba(0, 0, 0, 0.75)";
      self.octx.fillRect(0, 0, self.videoWidth, self.videoHeight);
      self.octx.fillStyle = "#f00";
      self.octx.fillRect(self.x, self.y, 5, 5);
      self.getPixelColor();
      console.log("setting pixel");
    },
    streamData: function() {
      self = this;
      self.peers = [
        new Peer(self.parameters),
        new Peer(self.parameters),
        new Peer(self.parameters)
      ];
      let index = 0;
      Object.keys(self.players).forEach(function(key) {
        self.peers[index].on("signal", function(data) {
          console.log(data);
          self.$socket.emit("newStreamPeer", {
            host: JSON.stringify(data),
            number: self.players[key].number
          });
        });
        index++;
      });
    },
    checkPeers: function() {
      self = this;
      self.database.ref("game/players").on("value", function(snapshot) {
        self.players = snapshot.val();

        let playing = 0;
        Object.keys(snapshot.val()).forEach(function(key) {
          if (self.players[key].playing) {
            ++playing;
            if (playing === 3) {
              self.streamData();
            }
          }
        });
      });
    },
    getVideo: function() {
      self = this;
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
          self.checkPeers();
          self.initializeCanvas();
        },
        function(error) {
          console.log("getUserMedia error: ", error);
        }
      );
    }
  },
  mounted() {
    this.getVideo();
    this.getSockets();
  }
};
</script>
