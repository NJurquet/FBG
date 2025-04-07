from threading import Timer
import time

class MyTimer:
    def __init__(self, time_needed, delete):
        self.time_needed = time_needed
        self.delete = delete
        self.startTime = time.time()
        self.timer = Timer(self.time_needed, self.delete)
        self.timer.start()

    def pause(self):
        self.timer.cancel()
        self.endTime = time.time()

    def resume(self, delete):
        self.delete = delete
        self.timer = Timer(self.time_needed-(self.endTime-self.startTime), self.delete)
        self.timer.start()

    def cancel(self):
        self.timer.cancel()
        self.timer = None