import socket
import time , ssl


def SchatWork(message):
	local_ip = socket.gethostbyname(socket.gethostname())
	HOST = local_ip
	PORT = 4589
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		s.send(message.encode("utf-8"))
		s.close()
	except ConnectionRefusedError:
		print(f"Connection refused. Couldn't send message: {message}")
		time.sleep(0.5)

	except ConnectionAbortedError:
		print(f"S Connection was aborted by the software on the host machine. Message: {message}")
		time.sleep(0.5)
	
	except ssl.SSLEOFError as e:
		print("S SSL EOF Error occurred. Retrying...")
		time.sleep(10)