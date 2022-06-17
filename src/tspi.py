import datetime
from collections import deque

class TSPIRecord:
    def __init__(self, x, y, z, heading, speed, time):
        self.x = x
        self.y = y
        self.z = z
        self.heading = heading
        self.speed = speed
        self.time = time

    def is_old(self, ttl, curr_time: datetime):
        return (curr_time - self.time).total_seconds() > ttl


class TSPIStore:
    def __init__(self, ttl):
        # Oldest record on right, the newest record on left
        self.records = deque()
        self.record_ttl = ttl

    def add_record(self, record: TSPIRecord):
        new_time = record.time
        while self.records[-1].is_old(self.record_ttl, new_time):
            self.records.pop()
