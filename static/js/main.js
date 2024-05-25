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

    // Function to send a custom event to the server
    function sendCustomEvent() {
        socket.emit('custom_event', {data: 'Test data'});  // Emit custom event with data
        //socket.send('Test socket message!');
    }

    // Add event listener to the button to send a custom event when clicked
    document.getElementById("sendCustomEvent").addEventListener("click", sendCustomEvent);

    // Handle the update_sellerList event
    socket.on('update_sellerList', function(data) {
        const productList = document.getElementById('sellerList');
        productList.innerHTML = '';  // Clear the list before adding new items

        data.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = `${item.name} - $${item.price}`;
            productList.appendChild(listItem);
        });
    });



});