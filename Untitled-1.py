import time
#from Untitled-2 import second2


def greet(name):
    print("Hello, " + name + "!")

def bye(name="Guest"):
    print("Bye, " + name + "!")


def first():
    Lanucher = True
    counter = 3
    while Lanucher == True:
        greet("Alice")
        greet("Bob")
        print("")
        time.sleep(0.1)
        counter = counter - 1
        if counter == 0:
            bye("Alice")
            bye()
            print("")
            Lanucher = False


def second():
    Lanucher = True
    counter = 13
    while Lanucher == True:
        greet("Alice")
        greet("Bob")
        print("")
        time.sleep(0.1)
        counter = counter - 1
        if counter == 0:
            bye("Alice")
            bye()
            print("")
            Lanucher = False



if __name__ == "__main__":
    first()
    second()