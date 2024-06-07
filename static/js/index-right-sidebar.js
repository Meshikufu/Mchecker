document.addEventListener("DOMContentLoaded", function() {
    const socket = io();
    // CPJ = control_panel.json

    // Load and apply the saved state from Local Storage
    var navbarRightButtons;
    const maxSearch = 10; // Maximum iterations to avoid infinite loop
    let containerFound = false; // Flag to check if a container is found in localStorage
    for (let i = 0; i < localStorage.length && i < maxSearch; i++) {
        const key = localStorage.key(i);
        if (key.startsWith('containerR')) {
            navbarRightButtons = localStorage.getItem(key);
            const element = document.getElementById(key);
            if (element) {
                element.classList.remove('hidden');
                element.classList.add('active');
                // Hide all other containers
                document.querySelectorAll('.right-sidebar-content.containerR').forEach(container => {
                    if (container.id !== key) {
                        container.classList.remove('active');
                        container.classList.add('hidden');
                    }
                });
                containerFound = true; // Set the flag to true
            }
            break; // Assuming there's only one such item, exit loop once found
        }
    }
    
    // If no container is found, hide all containers
    if (!containerFound) {
        document.querySelectorAll('.right-sidebar-content.containerR').forEach(container => {
            container.classList.remove('active');
            container.classList.add('hidden');
        });
    }

    // Listen for the create_buttons_CPJ event to create buttons dynamically
    socket.on('create_buttons_CPJ', function(data) {
        const container = document.getElementById('containerR1');
        container.innerHTML = '';  // Clear existing buttons

        for (const key in data) {
            if (data.hasOwnProperty(key)) {
                const value = data[key];
                const button = document.createElement('button');
                button.textContent = key;

                if (typeof value === 'boolean') {
                    button.className = 'boolean-buttons-CPJ ' + value;
                    button.addEventListener('click', function() {
                        const newValue = !data[this.textContent];
                        socket.emit('update_CPJ_value', { key: this.textContent, value: newValue });
                    });
                } else {
                    button.textContent = key + ' - ' + value;  // Display name and value for non-boolean
                    button.className = 'value-buttons-CPJ';
                    button.addEventListener('click', function() {
                        const currentKey = this.textContent.split(' - ')[0];
                        const currentValue = data[currentKey];
                        const newValue = prompt("Enter new value for " + currentKey, currentValue);

                        if (newValue !== null) {
                            // Try to convert to original type
                            if (!isNaN(currentValue)) {
                                newValue = currentValue % 1 === 0 ? parseInt(newValue) : parseFloat(newValue);
                            }
                            socket.emit('update_CPJ_value', { key: currentKey, value: newValue });
                        }
                    });
                }

                container.appendChild(button);
            }
        }
    });


    // Get all buttons with the class navbarRightButtons
    const buttons = document.querySelectorAll('.navbarRightButtons');

    // Add click event listener to each button
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            const buttonId = this.id;
            const containerNumber = buttonId.replace('navbarRightButton', '');
            toggleContainer(containerNumber);
        });
    });

    function toggleContainer(containerNumber) {
        const selectedContainer = document.getElementById('containerR' + containerNumber);
        if (selectedContainer) {
            const isActive = selectedContainer.classList.contains('active');
            if (isActive) {
                // If the container is active, hide it
                selectedContainer.classList.remove('active');
                selectedContainer.classList.add('hidden');
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    if (key.includes('containerR')) {
                        localStorage.removeItem(key);
                    }
                }
            } else {
                // Otherwise, hide all containers and show the selected one
                const containers = document.querySelectorAll('.containerR');
                containers.forEach(function(containerR) {
                    containerR.classList.remove('active');
                    containerR.classList.add('hidden');
                });
                selectedContainer.classList.remove('hidden');
                selectedContainer.classList.add('active');
                //console.log(selectedContainer);
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    if (key.includes('containerR')) {
                        localStorage.removeItem(key);
                    }
                }
                localStorage.setItem('containerR' + containerNumber, 'true');
            }
        }
    }
});
