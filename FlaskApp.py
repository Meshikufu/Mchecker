import socket
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, disconnect

from datetime import datetime
import json, os, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for session management and security
socketio = SocketIO(app)

# Define a route to serve the main page
@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML template for the main page

@socketio.on('connect') # when some one connects
def handle_connect():
    print('Client connected')  # Print a message to the server console

    try:
        with open('temp/SellerList.json', 'r') as json_file:
            loaded_data = json.load(json_file)
        socketio.emit('update_sellerList', loaded_data)
        
        start_timer_SellerList()
        emit_json_data()

    except Exception as e:
        print('SellerList.json doesnt exist')

def emit_json_data():
    try:
        with open('save/control_panel.json', 'r') as json_file:
            json_data = json.load(json_file)
        socketio.emit('create_buttons_CPJ', json_data)
    except Exception as e:
        print('Error reading control_panel.json:', e)

def start_timer_SellerList():
    try:
        stat = os.stat('temp/SellerList.json')
        modification_time = stat.st_mtime  # Modification time in seconds since epoch
        socketio.emit('starts_time_SellerList', {'startTime': modification_time})
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error occurred: {e}")

@socketio.on('update_CPJ_value')
def handle_update_value(data):
    try:
        with open('save/control_panel.json', 'r') as json_file:
            json_data = json.load(json_file)
        
        # Update the JSON data with the received data
        json_data[data['key']] = data['value']
        with open('save/control_panel.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        # Emit updated data to all clients
        emit_json_data()
    except Exception as e:
        print('Error updating control_panel.json:', e)

@socketio.on('message') # receiving
def handle_message(msg):
    if "SellerList" in msg:
        data = json.loads(msg)
        unwrapped_data = data["SellerList"]

        if not os.path.exists('temp'):
            os.makedirs('temp')
        json_data = json.dumps(unwrapped_data)
        with open('temp/SellerList.json', 'w') as json_file:
            json_file.write(json_data)

        current_datetime = datetime.now()
        print(current_datetime)
        #print(unwrapped_data)
        socketio.emit('update_sellerList', unwrapped_data)

        start_timer_SellerList()

        disconnect()
    else:
        print('recieved unknown message:')
        print(msg)
        print('disconnecting client!')
        disconnect()
        
@socketio.on('custom_event')
def handle_custom_event(data):
    print('Custom event received with data: ' + str(data))  # Print the received data to the server console
    emit('response', {'data': 'Custom event response'}, broadcast=True)  # Send a response to all clients

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')  # when client disconnects


# Get the local IPv4 address
ip_address = socket.gethostbyname(socket.gethostname())
# Run the Flask-SocketIO server on the local IPv4 address and port 8080
socketio.run(app, host=ip_address, port=8080, debug=True)