var Pusher = require('pusher');

var pusher = new Pusher({
    appId: '444197',
    key: '338fc3df23a162fc1144',
    secret: '77ef4433a16e0ae513b8',
    cluster: 'eu',
    encrypted: true
});

pusher.trigger('my-channel', 'my-event', {
    "message": "hello world"
});