import datetime
from collections import deque
import tspi_calc


class TSPIRecord:
    def __init__(self, x, y, z, x_speed, y_speed, time):
        # X, Y, Z in feet
        self.x = x
        self.y = y
        self.z = z

        # Speed in knots
        self.x_speed = x_speed
        self.y_speed = y_speed

        # Gets updated upon addition to a TSPIStore object
        self.d_x = 0
        self.d_y = 0

        # Time in datetime format
        self.time = time

    def is_old(self, ttl, curr_time: datetime):
        return (curr_time - self.time).total_seconds() > ttl


class TSPIStore:
    def __init__(self, ttl):
        # Oldest record on right, the newest record on left
        self.records = deque()
        self.record_ttl = ttl
        self.x_total_speed = 0
        self.y_total_speed = 0
        self.z_total_speed = 0

    def add_record(self, record: TSPIRecord):
        new_time = record.time
        tspi_calc.get_speed()
        self.x_total_speed += record.d_x
        self.y_total_speed += record.d_y
        self.z_total_speed += record.d_z

        while self.records[-1].is_old(self.record_ttl, new_time):
            self.x_total_speed -= self.records[-1].d_x
            self.y_total_speed -= self.records[-1].d_y
            self.z_total_speed -= self.records[-1].d_z
            self.records.pop()

    def get_newest_record(self):
        return self.records.popleft()

    def get_average_pos(self):
        record_len = len(self.records)
        return [self.x_total_speed/record_len, self.y_total_speed/record_len, self.z_total_speed/record_len]
