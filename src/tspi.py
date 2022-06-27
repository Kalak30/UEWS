"""Defines TSPIRecord and TSPIStore. These are used to store
Spacial and temporal information received in RSDF messages. """
import datetime
import logging
import tspi_calc
from recordclass import recordclass 
from collections import deque


logger = logging.getLogger(__name__)
Vector = recordclass("Vector", "x y z")


class TSPIRecord:
    """Represents the spacial and temporal data from a single RSDF message received from RDMS
        Calculates changes in x, y, and z positions between this record and previous record when added to TSPIStore
    """
    def __init__(self, position: Vector, speed: Vector, knots, heading, time):
        # sets the position, speed and heading
        self.position = Vector(0, 0, 0)
        self.speed = speed
        self.deltas = Vector(0, 0, 0)
        self.knots = 0
        self.heading = 0
        self.set_pose(position, knots, heading)

        # Time in datetime format
        self.time = time


    def is_old(self, ttl, curr_time: datetime):
        """Used to determine if this record is too old to keep around anymore
        :param ttl how long a record should be allowed to live
        :param curr_time the current time.
        :return boolean stating if record should be forgotten about"""
        return tspi_calc.get_time_diff(curr_time, self.time) > ttl

    
    def set_pose(self, pos: Vector, knots, heading):
        """Update position and knots, even if position is invalid
        :param pos Vector containing x, y, z coordinates of the position in sub
        :param knots speed in knots. Either calculated or received in message
        :param heading angle the sub is facing"""

        self.position = pos
        self.knots, self.heading = knots, heading

    def set_delta(self, x, y, z):
        self.deltas = Vector(x, y, z)

    def delta_from_record(self, other):
        """Sets the change in speed from this record to the other record in feet per second
        :param other Another record. Ideally used if other is the previous record created"""
        logger.debug(f"current x pos: {self.position.x}")
        logger.debug(f"past x pos: {other.position.x}")
        d_t = tspi_calc.get_time_diff(self.time, other.time)
        self.position.x = tspi_calc.get_delta(self.position.x, other.position.x, d_t)
        self.position.y = tspi_calc.get_delta(self.position.y, other.position.y, d_t)
        self.position.z = tspi_calc.get_delta(self.position.z, other.position.z, d_t)

    def print_values(self):
        """Prints values out to the logger"""
        logging.debug("Printing record values: ")
        logging.debug(f"x: {self.position.x}, y: {self.position.y}, z: {self.position.z}")
        logging.debug(f"d_x: {self.deltas.x}, d_y: {self.deltas.y}, d_z: {self.deltas.z} ")
        logging.debug(f"x_speed: {self.speed.x}, y_speed: {self.speed.y}")
        logging.debug(f"heading: {self.heading}, knots: {self.knots}, time: {self.time} ")
        logging.debug("end values printing\n")


class TSPIStore:
    """Store records in a Deque while their time is within the ttl
        Maintains sums of directional speeds to quicly calculate average speed over entire store
    """
    def __init__(self, ttl):
        # Oldest record on right, the newest record on left
        self.records = deque()
        self.record_ttl = ttl
        self.total_speeds = Vector(0, 0, 0)

    def increase_totals(self, deltas: Vector):
        """Increase the totals vector"""
        self.total_speeds.x += deltas.x
        self.total_speeds.y += deltas.y
        self.total_speeds.z += deltas.z


    def decrease_totals(self, deltas: Vector):
        """Decrease the totals tuple"""
        self.total_speeds.x -= deltas.x
        self.total_speeds.y -= deltas.y
        self.total_speeds.z -= deltas.z

    def add_record(self, record: TSPIRecord):
        """Adds a new record to the store. At the same time removes any stale records.
            Updates the total speed values when a record is added or deleted.
        :param record The TSPIRecord that needs to be added. Can be None
            """

        if record is None:
            return

        new_time = record.time

        # Check to make sure we don't access an empty record
        if len(self.records) == 0:
            record.set_delta(record.position.x, record.position.y, record.position.z)
        else:
            record.delta_from_record(self.records[0])

        # Update stored total speeds. Must create a new Vector tuple as tuples are immutable
        self.increase_totals(deltas=record.deltas)

        # Iterates through the oldest records, popping them off if they do not meet ttl
        # Also ensures that the total speeds are kept up to date
        while len(self.records) > 0 and self.records[-1].is_old(self.record_ttl, new_time):
            self.decrease_totals(deltas=self.records[-1].deltas)
            self.records.pop()
            logger.debug("Popped old record")

        self.records.appendleft(record)
        logging.debug(f"len after appending: {len(self.records)}")

    def get_newest_record(self):
        """Returns the newest (leftmost) record"""
        return self.records[0]

    def get_average_speeds(self):
        """Gets the average x, y, and z speeds using the maintained sums and length of Deque"""
        record_len = len(self.records)
        return [(k, val/record_len) for k, val in self.total_speeds]

    def print_all_records(self):
        """Prints all records within the store"""
        logging.debug("\nPrinting all records:\n")
        for record in self.records:
            record.print_values()
