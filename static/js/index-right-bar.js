document.addEventListener("DOMContentLoaded", function() {
    var socket = io();
    // CPJ = control_panel.json
    var buttonContainer_CPJ = document.getElementById('toggleButtonsHide_CPJ');
    var toggleButton_CPJ = document.getElementById('toggleButtonsShow_CPJ');

    // Listen for the create_buttons_CPJ event to create buttons dynamically
    socket.on('create_buttons_CPJ', function(data) {
        var container = document.getElementById('toggleButtonsHide_CPJ');
        container.innerHTML = '';  // Clear existing buttons

        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                var value = data[key];
                var button = document.createElement('button');
                button.textContent = key;

                if (typeof value === 'boolean') {
                    button.className = 'boolean-buttons-CPJ ' + value;
                    button.addEventListener('click', function() {
                        var newValue = !data[this.textContent];
                        socket.emit('update_CPJ_value', { key: this.textContent, value: newValue });
                    });
                } else {
                    button.textContent = key + ' - ' + value;  // Display name and value for non-boolean
                    button.className = 'value-buttons-CPJ';
                    button.addEventListener('click', function() {
                        var currentKey = this.textContent.split(' - ')[0];
                        var currentValue = data[currentKey];
                        var newValue = prompt("Enter new value for " + currentKey, currentValue);

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
            //toggleButton_CPJ.classList.add('hidden')
        } else {
            buttonContainer_CPJ.classList.add('hidden');
            toggleButton_CPJ.textContent = 'Show Buttons';
        }
    });
});