document.addEventListener("DOMContentLoaded", function() {
    const socket = io();
    // CPJ = control_panel.json
    const buttonContainer_CPJ = document.getElementById('toggleButtonsHide_CPJ');
    const toggleButton_CPJ = document.getElementById('toggleButtonsShow_CPJ');

    // Load and apply the saved state from Local Storage
    const buttonContainerState = localStorage.getItem('buttonContainerState_CPJ');
    if (buttonContainerState === 'visible') {
        buttonContainer_CPJ.classList.remove('hidden');
        toggleButton_CPJ.textContent = 'Hide Buttons';
    } else {
        buttonContainer_CPJ.classList.add('hidden');
        toggleButton_CPJ.textContent = 'Show Buttons';
    }

    // Listen for the create_buttons_CPJ event to create buttons dynamically
    socket.on('create_buttons_CPJ', function(data) {
        const container = document.getElementById('toggleButtonsHide_CPJ');
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

    toggleButton_CPJ.addEventListener('click', function() {
        if (buttonContainer_CPJ.classList.contains('hidden')) {
            buttonContainer_CPJ.classList.remove('hidden');
            toggleButton_CPJ.textContent = 'Hide Buttons';
            localStorage.setItem('buttonContainerState_CPJ', 'visible');
        } else {
            buttonContainer_CPJ.classList.add('hidden');
            toggleButton_CPJ.textContent = 'Show Buttons';
            localStorage.setItem('buttonContainerState_CPJ', 'hidden');
        }
    });
});
