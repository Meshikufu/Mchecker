import socket
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, disconnect

from datetime import datetime
import json, os
from modules.Refresh_ControlPanel_json import Refresh_ControlPanel_json

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
        onConnect_start_timer_SellerList()
        create_buttons_ControlPanelJson()
    except Exception as e:
        print('SellerList.json doesnt exist')
    SellerList_CheckRefreshButtonState()

def onConnect_start_timer_SellerList():
    try:
        stat = os.stat('temp/SellerList.json')
        modification_time = stat.st_mtime  # Modification time in seconds since epoch
        socketio.emit('onConnect_starts_time_SellerList', {'startTime': modification_time})
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_buttons_ControlPanelJson():
    try:
        with open('save/control_panel.json', 'r') as json_file:
            json_data = json.load(json_file)
        socketio.emit('create_buttons_CPJ', json_data)
    except Exception as e:
        print('Error reading control_panel.json:', e)

def SellerList_CheckRefreshButtonState():
    with open("temp/interrupt_signal.txt", "r") as signal_file:
        signal = signal_file.read().strip()
        if signal == "prep" or signal == "working":
            socketio.emit('refreshButtonState', "off")
        elif signal == "sleep":
            socketio.emit('refreshButtonState', "on")
        else:
            socketio.emit('killCat')


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

        onConnect_start_timer_SellerList()
        socketio.emit('refreshButtonState', "on")

        disconnect()
    else:
        print('recieved unknown message:')
        print(msg)
        print('disconnecting client!')
        disconnect()


        
        
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')  # when client disconnects





@socketio.on('waitFor_ButtonRefreshSellerList')
def waitForButtonEnable():
    initial_mtime = os.path.getmtime('temp/SellerList.json')
    
    while True:
        # Check if the modification time has changed
        current_mtime = os.path.getmtime('temp/SellerList.json')
        if current_mtime != initial_mtime:
            socketio.emit('refreshButtonState', "on")
            print('json updated!')
            break
        socketio.sleep(0.5)

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
        create_buttons_ControlPanelJson()
    except Exception as e:
        print('Error updating control_panel.json:', e)

@socketio.on('refresh_sellerList')
def handle_custom_event():

    prep_found = False
    with open("temp/interrupt_signal.txt", "r") as file:
        for line in file:
            if "prep" in line:
                prep_found = True
                break
    if prep_found is False:
        with open("temp/interrupt_signal.txt", "w") as signal_file:
            signal_file.write("interrupt")


# Get the local IPv4 address
ip_address = socket.gethostbyname(socket.gethostname())
# Run the Flask-SocketIO server on the local IPv4 address and port 8080
socketio.run(app, host=ip_address, port=8080, debug=True)