import socket
import time

def Schat(message):
	HOST = socket.gethostname()
	PORT = 1235
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		#print(f'{message}')
		s.send(message.encode("utf-8"))
		s.close()
	except ConnectionRefusedError:
		print(f"Connection refused. Couldn't send message: {message}")
		#print(f'{message}')
		time.sleep(0.5)

def Schat2(message2):
	HOST = socket.gethostname()
	PORT = 1235
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		#print(f'{message}')
		s.send(message2.encode("utf-8"))
		s.close()
	except ConnectionRefusedError:
		print(f"Connection refused. Couldn't send message: {message2}")
		#print(f'{message}')
		time.sleep(0.5)