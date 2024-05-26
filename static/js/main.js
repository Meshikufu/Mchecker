document.addEventListener("DOMContentLoaded", function() {

    // Establish connection with the server
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Handle connection event
    socket.on('connect', function() {
        console.log('Connected to server');  // Log connection message to the console
    });

    // Handle incoming messages
    socket.on('message', function(msg) {
        console.log('Message received: ' + msg);  // Log received message to the console
    });

    // Handle custom event responses
    socket.on('response', function(data) {
        console.log('Custom event response: ' + data.data);  // Log response to the console
    });


});