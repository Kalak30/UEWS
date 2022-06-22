import datetime
from collections import deque
import logging
import tspi_calc
from alert_msgs import invalid_data_alert

logger = logging.getLogger(__name__)


# Represents the spacial and temporal data from a single RSDF message received from RDMS
# Validates whether a supplied position and knots is normal
# Calculates changes in x, y, and z positions between this record and previous record when added to TSPIStore
class TSPIRecord:
    def __init__(self, x, y, z, x_speed, y_speed, knots, heading, time):
        # sets the position, speed and heading after doing a validation check
        self.position = {"x": 0, "y": 0, "z": 0}
        self.speed = {"x": x_speed, "y": y_speed, "z": 0}
        self.deltas = {"x": 0, "y": 0, "z": 0}
        self.knots = 0
        self.heading = 0
        self.set_pose(x, y, z, knots, heading)

        # Time in datetime format
        self.time = time

        # Whether the position data is within the specified normal range
        self.valid = True

    def is_old(self, ttl, curr_time: datetime):
        return tspi_calc.get_time_diff(curr_time, self.time) > ttl

    # Update position and knots, even if position is invalid
    def set_pose(self, x, y, z, knots, heading):
        self.valid = tspi_calc.validate_pos(x, y, z, knots)
        self.position = {x, y, z}
        self.knots, self.heading = knots, heading

    def set_delta(self, x, y, z):
        self.deltas = {x, y, z}

    # sets the change in speed from this record to the other record in feet per second
    def delta_from_record(self, other):
        logger.debug(f"current x pos: {self.position['x']}")
        logger.debug(f"past x pos: {other.position['x']}")
        d_t = tspi_calc.get_time_diff(self.time, other.time)
        self.deltas["x"] = tspi_calc.get_delta(self.position['x'], other.x, d_t)
        self.deltas["y"] = tspi_calc.get_delta(self.position['y'], other.y, d_t)
        self.deltas["z"] = tspi_calc.get_delta(self.position['z'], other.z, d_t)

    def print_values(self):
        logging.debug("Printing record values: ")
        logging.debug(f"x: {self.position['x']}, y: {self.position['y']}, z: {self.position['z']}")
        logging.debug(f"d_x: {self.deltas['x']}, d_y: {self.deltas['y']}, d_z: {self.deltas['z']} ")
        logging.debug(f"x_speed: {self.speed['x']}, y_speed: {self.speed['y']}")
        logging.debug(f"heading: {self.heading}, knots: {self.knots}, time: {self.time} ")
        logging.debug("end values printing\n")


# Store records in a Deque while their time is within the ttl
# Maintains sums of directional speeds to quicly calculate average speed over entire store
# Alerts if attempting to add an invalid record
class TSPIStore:
    def __init__(self, ttl):
        # Oldest record on right, the newest record on left
        self.records = deque()
        self.record_ttl = ttl
        self.total_speeds = {"x": 0, "y": 0, "z": 0}

    def add_record(self, record: TSPIRecord):
        if record is None:
            return
        # record is invalid and we should alert
        if not record.valid:
            invalid_data_alert()
            return

        new_time = record.time

        # Check to make sure we don't access an empty record
        if len(self.records) == 0:
            record.set_delta(record.position['x'], record.position['y'], record.position['z'])
        else:
            record.delta_from_record(self.records[0])

        # Update stored total speeds
        self.total_speeds['x'] += record.deltas['x']
        self.total_speeds['y'] += record.deltas['y']
        self.total_speeds['z'] += record.deltas['z']

        # Iterates through the oldest records, popping them off if they do not meet ttl
        # Also ensures that the total speeds are kept up to date
        while len(self.records) > 0 and self.records[-1].is_old(self.record_ttl, new_time):
            self.total_speeds['x'] -= self.records[-1].deltas['x']
            self.total_speeds['y'] -= self.records[-1].deltas['y']
            self.total_speeds['z'] -= self.records[-1].deltas['z']
            self.records.pop()
            logger.debug("Popped old record")

        self.records.appendleft(record)
        logging.debug(f"len after appending: {len(self.records)}")

    # Returns the newest (leftmost) record
    def get_newest_record(self):
        return self.records[0]

    # Gets the average x, y, and z speeds using the maintained sums and length of Deque
    def get_average_speeds(self):
        record_len = len(self.records)
        return [(k, val/record_len) for k, val in self.total_speeds]

    def print_all_records(self):
        logging.debug("\nPrinting all records:\n")
        for record in self.records:
            record.print_values()
