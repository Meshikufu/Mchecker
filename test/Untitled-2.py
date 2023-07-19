import time
from modules.SocketClient import Schat
import socket

HOST = socket.gethostname()
PORT = 1235

def greet(name):
    print("Hello, " + name + "!")

def bye(name="Guest"):
    print("Bye, " + name + "!")


def sendcounter(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(message.encode("utf-8"))
    s.close()

def sendcounter2(message2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(message2.encode("utf-8"))
    s.close()


def second2():
    Lanucher = True
    counter = 113
    counter2 = 153
    counter3 = 123

    while Lanucher == True:
        greet("Alice")
        greet("Bob")
        print("")



        message = str(counter)
        message2 = str(counter2)
        message3 = str(counter3)
        #Schat(message)



        sendcounter(message)
        sendcounter2(message2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(message3.encode("utf-8"))
        

        time.sleep(0.101)
        counter = counter - 1
        counter2 = counter2 - 1
        counter3 = counter3 - 1
        if counter == 0:
            bye("Alice")
            bye()
            print("")
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.sendall(b'change_icon_alert')
            Lanucher = False

        s.close()





if __name__ == "__main__":
    second2()