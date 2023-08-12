import socket
import time , ssl

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

	except ConnectionAbortedError:
		# Code to handle the ConnectionAbortedError
		print(f"S Connection was aborted by the software on the host machine. Message: {message}")
		time.sleep(0.5)
	
	except ssl.SSLEOFError as e:
		print("S SSL EOF Error occurred. Retrying...")
		time.sleep(10)

#def Schat2(message2):
#	HOST = socket.gethostname()
#	PORT = 1235
#	try:
#		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#		s.connect((HOST, PORT))
#		#print(f'{message}')
#		message = message2
#		s.send(message.encode("utf-8"))
#		s.close()
#	except ConnectionRefusedError:
#		print(f"Connection refused. Couldn't send message: {message2}")
#		#print(f'{message}')
#		time.sleep(0.5)
#
#	except ConnectionAbortedError:
#		# Code to handle the ConnectionAbortedError
#		print(f"S Connection was aborted by the software on the host machine. Message: {message2}")
#		time.sleep(0.5)
#	
#	except ssl.SSLEOFError as e:
#		print("S SSL EOF Error occurred. Retrying...")
#		time.sleep(10)