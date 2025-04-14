from threading import Timer
import time

class MyTimer:
    def __init__(self, time_needed, delete):
        self._time_needed = time_needed
        self._delete = delete
        self._startTime = time.time()
        self._elapsedTime = 0  
        self._timer = Timer(self._time_needed, self._delete)
        self._timer.start()

    def pause(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None
            self.endTime = time.time()
            self._elapsedTime += (self.endTime - self._startTime)

    def resume(self, delete) -> float:
        self._startTime = time.time()
        self._delete = delete
        self._time_needed = max(0, self._time_needed - self._elapsedTime)
        self._elapsedTime = 0 
        
        self._timer = Timer(self._time_needed, self._delete)
        self._timer.start()

        return self._time_needed

    def cancel(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None