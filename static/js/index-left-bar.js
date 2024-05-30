document.addEventListener("DOMContentLoaded", function() {
    var socket = io();
    var timerInterval;


    //socket.on('killCat', function() {
    //    const gif = document.getElementById("catGif");
    //    gif.style.display = "none";
   // });



    function refreshButtonStateOn(){
        const button = document.getElementById("buttonRefreshSellerList");
        const gif = document.getElementById("catGif");
        button.disabled = false;  // Re-enable the button
        button.classList.add("buttonRefreshSellerList-hover", "buttonRefreshSellerList-active", "buttonRefreshSellerList-focus");
        button.style.cursor = "pointer";  // Reset the cursor
        button.style.opacity = "1";  // Restore the button appearance
        gif.style.display = "none";
    };

    function refreshButtonStateOff(){
        const button = document.getElementById("buttonRefreshSellerList");
        const gif = document.getElementById("catGif");
        button.disabled = true;  // Disable the button
        button.classList.remove("buttonRefreshSellerList-hover", "buttonRefreshSellerList-active", "buttonRefreshSellerList-focus");
        button.style.cursor = "not-allowed";  // Change the cursor to not-allowed
        button.style.opacity = "0.6";  // Dim the button
        gif.style.display = "Inline";
    };


    socket.on('refreshButtonState', function(buttonState) {
        if (buttonState === "on"){
            refreshButtonStateOn()
        } else if (buttonState === "off") {
            refreshButtonStateOff()
        }
    });


    // Function to send a custom event to the server
    function buttonRefreshSellerList() {
        socket.emit('refresh_sellerList');
        socket.emit('checkStateOf_sellerList');
        refreshButtonStateOff();
        socket.emit('waitFor_ButtonRefreshSellerList');
    }

    // Add event listener to the button to send a custom event when clicked
    document.getElementById("buttonRefreshSellerList").addEventListener("click", buttonRefreshSellerList);

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
            //console.log(seconds)

            // Update the timer value in the <h3> element
            document.getElementById('startTimer').textContent = seconds + 's';
        }

        // Initial call to update the timer immediately
        updateTimer();
        // Update the timer every second
        timerInterval = setInterval(updateTimer, 1000); // Update the timer every second (1000 milliseconds)
    }

    // Socket event handler to start the timer
    socket.on('onConnect_starts_time_SellerList', function(data) {
        startTimer(data ? data.startTime : null); // Call the startTimer function with the modification time if available
    });

});