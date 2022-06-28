"""Defines TSPIRecord and TSPIStore. These are used to store
Spacial and temporal information received in RSDF messages. """
import datetime
import logging
from tspi_calc import get_time_diff, get_delta, get_predict_given, get_predict_custom
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
        self.proj_position = Vector(0,0,0)

        # Time in datetime format
        self.time = time


    def is_old(self, ttl, curr_time: datetime):
        """Used to determine if this record is too old to keep around anymore
        :param ttl how long a record should be allowed to live
        :param curr_time the current time.
        :return boolean stating if record should be forgotten about"""
        return get_time_diff(curr_time, self.time) > ttl

    
    def set_pose(self, pos: Vector, knots, heading):
        """Update position and knots, even if position is invalid
        :param pos Vector containing x, y, z coordinates of the position in sub
        :param knots speed in knots. Either calculated or received in message
        :param heading angle the sub is facing"""

        self.position = pos
        self.knots, self.heading = knots, heading

    def set_delta(self):
        self.deltas = Vector(0,0,0)

    def delta_from_record(self, other):
        """Sets the change in speed from this record to the other record in feet per second
        :param other Another record. Ideally used if other is the previous record created"""
        logger.debug(f"current x pos: {self.position.x}")
        logger.debug(f"past x pos: {other.position.x}")
        d_t = get_time_diff(self.time, other.time)
        self.deltas.x = get_delta(self.position.x, other.position.x, d_t)
        self.deltas.y = get_delta(self.position.y, other.position.y, d_t)
        self.deltas.z = get_delta(self.position.z, other.position.z, d_t)

    def print_values(self):
        """Prints values out to the logger"""
        logger.debug("Printing record values: ")
        logger.debug(f"x: {self.position.x}, y: {self.position.y}, z: {self.position.z}")
        logger.debug(f"d_x: {self.deltas.x}, d_y: {self.deltas.y}, d_z: {self.deltas.z} ")
        logger.debug(f"x_speed: {self.speed.x}, y_speed: {self.speed.y}")
        logger.debug(f"heading: {self.heading}, knots: {self.knots}, time: {self.time} ")
        logger.debug(f"proj_x: {self.proj_position.x}, proj_y: {self.proj_position.y}, proj_z: {self.proj_position.z}")
        logger.debug("end values printing\n")


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
            record.set_delta()
        else:
            record.delta_from_record(self.records[0])

        # Update stored total speeds. Must create a new Vector tuple as tuples are immutable
        #only update if at leaste 2 records
        self.increase_totals(deltas=record.deltas)

        # Iterates through the oldest records, popping them off if they do not meet ttl
        # Also ensures that the total speeds are kept up to date
        while len(self.records) > 0 and self.records[-1].is_old(self.record_ttl, new_time):
            self.decrease_totals(deltas=self.records[-1].deltas)
            self.records.pop()
            logger.debug("Popped old record")


        self.records.appendleft(record)
        logger.debug(f"len after appending: {len(self.records)}")

        
    def get_prediction(self, record: TSPIRecord, custom):
        if custom:
            avg_speeds = self.get_average_speeds()
            record.proj_position = get_predict_custom(record.position, avg_speeds, 300)
            return
        else:
            record.proj_position = get_predict_given(record.position, record.speed, 300) #TODO change seconds param to be configurable

    def get_predict_given(self, position, speed, seconds):
        """Calculate the projected position of the sub according to the given code 11 track's of speed and heading. 
        Does NOT take into account z speed (how fast depth changes)
        return: vector of the position"""
        #z value should just stay the same here
        proj_position = Vector(0,0,0)
        proj_position.x = position.x + (speed.x * seconds)
        proj_position.y = position.y + (speed.y * seconds)
        proj_position.z = position.z

        logger.debug("Using given predictions")
        logger.debug(f"Input position: {position}")
        logger.debug(f"Given Speed: {speed}, seconds: {seconds}")
        logger.debug(f"Predicted Position: {proj_position}")

        return proj_position

    def get_predict_custom(self, position, avg_speeds, seconds):
        """Calculates the projected position of the sub using the past x number of valid positions. 
        This DOES take into account z speed."""
        proj_position = proj_position = Vector(0,0,0)
        proj_position.x = position.x + (avg_speeds.x * seconds)
        proj_position.y = position.y + (avg_speeds.y * seconds)
        proj_position.z = position.z + (avg_speeds.z * seconds)

        logger.debug("Using custonm predictions")
        logger.debug(f"Input position: {position}")
        logger.debug(f"Predicted Position: {proj_position}")

        return proj_position

    def get_newest_record(self):
        """Returns the newest (leftmost) record"""
        return self.records[0]

    def get_average_speeds(self):
        """Gets the average x, y, and z speeds using the maintained sums and length of Deque"""
        record_len = len(self.records)
        avg_speed = Vector(0,0,0)
        if record_len == 1:
            return avg_speed

        avg_speed.x = self.total_speeds.x/record_len
        avg_speed.y = self.total_speeds.y/record_len
        avg_speed.z = self.total_speeds.z/record_len

        return avg_speed

    def print_all_records(self):
        """Prints all records within the store"""
        logger.debug("\nPrinting all records:\n")
        for record in self.records:
            record.print_values()
