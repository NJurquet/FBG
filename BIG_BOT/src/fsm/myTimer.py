from threading import Timer
import time

class MyTimer:
    def __init__(self, time_needed, delete):
        self.time_needed = time_needed
        self.delete = delete
        self.startTime = time.time()
        self.elapsedTime = 0  
        self.timer = Timer(self.time_needed, self.delete)
        self.timer.start()

    def pause(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
            self.endTime = time.time()
            self.elapsedTime += (self.endTime - self.startTime)

    def resume(self, delete) -> float:
        self.startTime = time.time()
        self.delete = delete
        self.time_needed = max(0, self.time_needed - self.elapsedTime)
        self.elapsedTime = 0 
        
        self.timer = Timer(self.time_needed, self.delete)
        self.timer.start()

        return self.time_needed

    def cancel(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None