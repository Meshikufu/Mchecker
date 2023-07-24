from threading import Thread
import time

class LoopThreads:
    def __init__(self):
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0

    def mainLoop(self):
        self.counter1 = 0
        while True:
            self.counter1 += 1
            print("Counter1:", self.counter1)
            time.sleep(0.2)
            if self.counter1 == 30:
                self.secondLoop()

            if self.counter1 == 80:
                self.counter1 = 0
                self.secondLoop()
                self.thirdLoop()
                break

    def secondLoop(self):
        self.counter2 = 0
        while True:
            self.counter2 += 1
            print("Counter2:", self.counter2)
            time.sleep(0.2)
            if self.counter2 == 15:
                self.counter2 = 0
                break

    def thirdLoop(self):
        self.counter3 = 0
        while True:
            self.counter3 += 1
            print("Counter3:", self.counter3)
            time.sleep(0.2)
            if self.counter3 >= 45 and self.counter1 == 0 and self.counter2 == 0:
                self.counter3 = 0
                self.mainLoop()
                break

loop_threads = LoopThreads()

thread1 = Thread(target=loop_threads.mainLoop)
thread2 = Thread(target=loop_threads.secondLoop)
thread3 = Thread(target=loop_threads.thirdLoop)

thread1.start()
thread2.start()
thread3.start()