import numpy as np

class RingBuffer:
    def __init__(self, size=50):
        self.size = size
        self.buffer = []

    def add(self, value):
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)
        self.buffer.append(value)

    def is_ready(self):
        return len(self.buffer) >= self.size

    def get_all(self):
        return np.array(self.buffer)