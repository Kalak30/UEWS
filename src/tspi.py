from asyncio.windows_events import NULL
import datetime
from collections import deque
from types import NoneType
import tspi_calc
from statics import *
from alert_msgs import invalid_data_alert


# Represents the spacial and temporal data from a single RSDF message received from RDMS
# Validates whether a supplied position and knots is normal
# Calculates changes in x, y, and z positions between this record and previous record when added to TSPIStore
class TSPIRecord:
    def __init__(self, x, y, z, x_speed, y_speed, knots, heading, time):
        # sets the position, speed and heading after doing a validation check
        self.x = 0
        self.y = 0
        self.z = 0
        self.knots = 0
        self.heading = 0
        self.set_pose(x, y, z, knots, heading)

        # Speed in feet per second
        self.x_speed = x_speed
        self.y_speed = y_speed

        # Gets updated upon addition to a TSPIStore object
        self.z_speed = 0
        self.d_x = 0
        self.d_y = 0
        self.d_z = 0

        # Time in datetime format
        self.time = time

        # Whether the position data is within the specified normal range
        self.valid = True

    def is_old(self, ttl, curr_time: datetime):
        return tspi_calc.get_time_diff(curr_time, self.time) > ttl

    def set_pose(self, x, y, z, knots, heading):
        self.validate_pos()
        self.x, self.y, self.z, self.knots, self.heading = x, y, z, knots, heading

    def set_delta(self, x, y, z):
        self.d_x = x
        self.d_y = y
        self.d_z = z

    # sets the change in speed from this record to the other record in feet per second
    def delta_from_record(self, other):
        d_t = tspi_calc.get_time_diff(self.time, other.time)
        self.d_x = tspi_calc.get_delta(self.x_speed, other.x_speed, d_t)
        self.d_y = tspi_calc.get_delta(self.y_speed, other.x_speed, d_t)
        self.d_z = tspi_calc.get_delta(self.z_speed, other.x_speed, d_t)

    # Gets called upon creation and changing the pose of the record
    def validate_pos(self):
        if self.x < x_outlier["lower"] or self.x > x_outlier["upper"] or self.y < y_outlier["lower"] or \
                self.y > y_outlier["upper"] or self.z < z_outlier["lower"] or self.z > z_outlier["upper"] or \
                self.knots > speed_outlier["upper"]:
            self.valid = False
            return
        self.valid = True


# Store records in a Deque while their time is within the ttl
# Maintains sums of directional speeds to quicly calculate average speed over entire store
# Alerts if attempting to add an invalid record
class TSPIStore:
    def __init__(self, ttl):
        # Oldest record on right, the newest record on left
        self.records = deque()
        self.record_ttl = ttl
        self.x_total_speed = 0
        self.y_total_speed = 0
        self.z_total_speed = 0

    def add_record(self, record: TSPIRecord):
        if record == NULL:
            return
        # record is invalid and we should alert
        if not record.valid:
            invalid_data_alert()
            return

        new_time = record.time

        # Check to make sure we don't access an empty record
        if len(self.records) == 0:
            record.set_delta(record.x, record.y, record.z)
        else:
            record.delta_from_record(self.records[0])

        # Update stored total speeds
        self.x_total_speed += record.d_x
        self.y_total_speed += record.d_y
        self.z_total_speed += record.d_z

        # Iterates through the oldest records, popping them off if they do not meet ttl
        # Also ensures that the total speeds are kept up to date
        while len(self.records) > 0 and self.records[-1].is_old(self.record_ttl, new_time):
            self.x_total_speed -= self.records[-1].d_x
            self.y_total_speed -= self.records[-1].d_y
            self.z_total_speed -= self.records[-1].d_z
            self.records.pop()
        
        self.records.appendleft(record)

    # Returns the newest (leftmost) record
    def get_newest_record(self):
        return self.records.popleft()

    # Gets the average x, y, and z speeds using the maintained sums and length of Deque
    def get_average_speeds(self):
        record_len = len(self.records)
        return [self.x_total_speed/record_len, self.y_total_speed/record_len, self.z_total_speed/record_len]
