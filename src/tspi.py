import datetime
from collections import deque


class TSPIRecord:
    def __init__(self, x, y, z, x_speed, y_speed, time):
        # X, Y, Z in feet
        self.x = x
        self.y = y
        self.z = z

        # Speed in knots
        self.x_speed = x_speed
        self.y_speed = y_speed

        # Time in datetime format
        self.time = time

    def is_old(self, ttl, curr_time: datetime):
        return (curr_time - self.time).total_seconds() > ttl


class TSPIStore:
    def __init__(self, ttl):
        # Oldest record on right, the newest record on left
        self.records = deque()
        self.record_ttl = ttl
        self.x_sum = 0
        self.y_sum = 0
        self.z_sum = 0

    def add_record(self, record: TSPIRecord):
        new_time = record.time
        self.x_sum += record.x
        self.y_sum += record.y
        self.z_sum += record.z

        while self.records[-1].is_old(self.record_ttl, new_time):
            self.x_sum -= self.records[-1].x
            self.y_sum -= self.records[-1].y
            self.z_sum -= self.records[-1].z
            self.records.pop()

    def get_newest_record(self):
        return self.records.popleft()

    def get_average_pos(self):
        record_len = len(self.records)
        return [self.x_sum/record_len, self.y_sum/record_len, self.z_sum/record_len]
