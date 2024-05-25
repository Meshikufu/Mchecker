document.addEventListener("DOMContentLoaded", function() {
    // Initialize the socket object
    var socket = io();
    var timerInterval;

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


    socket.on('starts_time_SellerList', function(data) {
        startTimer(data ? data.startTime : null); // Call the startTimer function with the modification time if available
    });
    function startTimer(startTime) {
        if (!startTime) {
            startTime = Date.now() / 1000; // Use current time if startTime is not provided
        }

        if (timerInterval) {
            clearInterval(timerInterval); // Clear any existing interval
        }

        function updateTimer() {
            const currentTime = Date.now(); // Get the current timestamp in milliseconds
            const elapsedTime = currentTime - startTime * 1000; // Calculate elapsed time in milliseconds

            // Convert elapsed time to seconds
            const seconds = Math.floor(elapsedTime / 1000);

            // Update the timer value in the <h3> element
            document.getElementById('startTimer').textContent = seconds + 's';
        }

        // Initial call to update the timer immediately
        updateTimer();
        // Update the timer every second
        timerInterval = setInterval(updateTimer, 1000); // Update the timer every second (1000 milliseconds)
    }

    // Socket event handler to start the timer
    socket.on('starts_time_SellerList', function(data) {
        startTimer(data ? data.startTime : null); // Call the startTimer function with the modification time if available
    });

});