import socket
from modules.SocketClient import Schat

def socketServer(tray, chatMain):
	chatMain = chatMain
	tray = tray
	HOST = socket.gethostname()
	PORT = 1235

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(5)

	print("Socket server started successfully!")

	while True:
		clientsocket, address = s.accept()
		print(f"Connection from {address} has been established!")

		# Receive the message from the client
		message = clientsocket.recv(1024).decode("utf-8")

		print("Received message:")
		print(message)

		if message == "change_icon_alert":
			tray.change_icon('pic/alert.png')
		elif message == "start_sleep_bar2":
			chatMain.start_sleep_bar2()	
		else:
			chatMain.add_log_message(message)
			chatMain.add_log_message("")

		# Process the received message as needed
		clientsocket.close()