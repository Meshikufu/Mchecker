document.addEventListener("DOMContentLoaded", function() {
    const socket = io();
    var timerInterval;

    //socket.on('killCat', function() {
    //    const gif = document.getElementById("catGif");
    //    gif.style.display = "none";
   // });



    function refreshButtonStateOn() {
        const elementIds = ["buttonRefreshSellerList", "buttonNewPrice", "buttonOnline", "buttonOffline", "catGif"];

        elementIds.forEach(id => {
            const element = document.getElementById(id);
            
            if (element) {
                if (id.startsWith("button")) {
                    element.disabled = false;
                    element.classList.add(`${id}-hover`, `${id}-active`, `${id}-focus`);
                    element.style.cursor = "pointer";
                    element.style.opacity = "1";
                } else if (id === "catGif") {
                    element.style.display = "none";
                }
            }
        });
    }

    function refreshButtonStateOff() {
        const elementIds = ["buttonRefreshSellerList", "buttonNewPrice", "buttonOnline", "buttonOffline", "catGif"];

        elementIds.forEach(id => {
            const element = document.getElementById(id);
            
            if (element) {
                if (id.startsWith("button")) {
                    element.disabled = true;
                    element.classList.remove(`${id}-hover`, `${id}-active`, `${id}-focus`);
                    element.style.cursor = "not-allowed";
                    element.style.opacity = "0.6";
                } else if (id === "catGif") {
                    element.style.display = "inline";
                }
            }
        });
    }


    socket.on('refreshButtonState', function(buttonState) {
        if (buttonState === "on"){
            refreshButtonStateOn()
        } else if (buttonState === "off") {
            refreshButtonStateOff()
        }
    });


    // Function to send a custom event to the server
    function buttonRefreshSellerList() {
        socket.emit('buttonRefresh_sellerList');
        socket.emit('checkStateOf_sellerList');
        refreshButtonStateOff();
        socket.emit('waitFor_ButtonRefreshSellerList');
    }

    // Add event listener to the button to send a custom event when clicked
    document.getElementById("buttonRefreshSellerList").addEventListener("click", buttonRefreshSellerList);


    function handleButtonClick(eventType, data = 0) {
        const buttonBlockName = 'buttonSellerList'
        switch (eventType) {
            case 'change_price':
                let newPrice = prompt("Enter new price");
                if (newPrice !== null) {
                    console.log(newPrice);
                    socket.emit(buttonBlockName, eventType, parseFloat(newPrice));
                }
                break;
            case 'change_to_online':
                socket.emit(buttonBlockName, eventType, data);
                break;
            case 'change_to_offline':
                socket.emit(buttonBlockName, eventType, data);
                break;
            default:
                console.error("Unknown event type:", eventType);
                break;
        }
    }
    
    document.getElementById("buttonNewPrice").addEventListener("click", function() {
        handleButtonClick('change_price');
    });
    
    document.getElementById("buttonOnline").addEventListener("click", function() {
        handleButtonClick('change_to_online');
    });
    
    document.getElementById("buttonOffline").addEventListener("click", function() {
        handleButtonClick('change_to_offline');
    });

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