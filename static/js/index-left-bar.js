document.addEventListener("DOMContentLoaded", function() {
    // Initialize the socket object
    var socket = io();
    var timerInterval;


    // Function to send a custom event to the server
    function refreshSellerList() {
        const button = document.getElementById("refreshSellerList");
        button.disabled = true;  // Disable the button
        button.style.cursor = "not-allowed";  // Change the cursor to not-allowed
        button.style.opacity = "0.6";  // Dim the button
    
        socket.emit('refresh_sellerList');  // Emit custom event with data
    
        // Re-enable the button after 10 seconds
        setTimeout(() => {
            button.disabled = false;  // Re-enable the button
            button.style.cursor = "pointer";  // Reset the cursor
            button.style.opacity = "1";  // Restore the button appearance
        }, 10000);  // 10000 milliseconds = 10 seconds
    }

    // Add event listener to the button to send a custom event when clicked
    document.getElementById("refreshSellerList").addEventListener("click", refreshSellerList);

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