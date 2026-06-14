import time

class EventLogger:
    def __init__(self):
        self.events = []

    def log(self, x, y, direction):
        self.events.append({
            "x": x,
            "y": y,
            "direction": direction,
            "timestamp": time.time()
        })

    def get_recent(self, n=20):
        return self.events[-n:]

    def total(self):
        return len(self.events)