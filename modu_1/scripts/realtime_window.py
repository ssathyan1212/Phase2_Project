# scripts/realtime_window.py
from collections import deque
class SlidingWindow:
    def __init__(self, size=16):
        self.window = deque(maxlen=size)

    def add(self, value):
        self.window.append(value)

    def is_ready(self):
        return len(self.window) == self.window.maxlen

    def get(self):
        return list(self.window)
