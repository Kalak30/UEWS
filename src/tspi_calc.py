import math
from tspi import Vector
from statics import *
import logging

logger = logging.getLogger(__name__)

def get_delta(s1, s2, seconds):
    return (s1 - s2) / seconds


# get my_speed in yards per second
def get_speed(my_speed, current_position, last_position, seconds):
    # alternatively this can be done by using the given my_speed and heading.
    logger.debug(current_position[0])
    logger.debug(last_position[0])
    # calculated my_speed in each direction with current and last positions (each position is in yards)
    logger.debug("seconds: ", seconds)
    my_speed[0] = (current_position[0] - last_position[0]) / seconds
    my_speed[1] = (current_position[1] - last_position[1]) / seconds
    my_speed[2] = (current_position[2] - last_position[2]) / seconds


# calculate speed in x and y direction from the given knots and heading values
def get_speed_from_knots(knots, heading):
    # rotate 90 so that head is degrees off of x-axis (instead of y-axis) ((or y instead of x, not sure))
    heading = heading - 90
    # print("incoming knots : ",my_knots,"incoming heading: ",heading)
    x_speed = (1.68781 * (knots * math.sin((math.radians(heading)))))
    y_speed = (1.68781 * (knots * math.cos((math.radians(heading)))))
    return x_speed, y_speed


# calculate knots from calculated speed from given positioning
def get_knots(my_speed):
    # 1 yard/second = 1.77745 my_knots
    # totalSpeed = math.sqrt(my_speed[0]**2 + my_speed[1]**2 + my_speed[2]**2)
    xy_speed = math.sqrt((my_speed[0]) ** 2 + (my_speed[1] ** 2))
    total_speed = math.sqrt(xy_speed ** 2 + (my_speed[2]) ** 2)

    logger.debug("xy_speed:     ", xy_speed)
    logger.debug("total speed: ", total_speed)

    # total_knots = totalSpeed * 0.592484
    total_knots = xy_speed * 0.592484

    # note: incoming knots only account for xy directions
    return total_knots


def get_time_diff(input_time, last_time):
    time_diff = input_time - last_time
    seconds = abs(time_diff.total_seconds())

    # Check if no time diff, avoids divide by zero error
    if seconds == 0:
        logger.debug("no time difference")
        seconds = 1000000

    return seconds

def get_predict_given(position, speed, seconds):
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

def get_predict_custom(position, avg_speeds, seconds):
    """Calculates the projected position of the sub using the past x number of valid positions. 
    This DOES take into account z speed."""
    proj_position = proj_position = Vector(0,0,0)
    proj_position.x = position.x + (avg_speeds.x * seconds)
    proj_position.y = position.y + (avg_speeds.y * seconds)
    proj_position.z = position.z + (avg_speeds.z * seconds)

    logger.debug("Using custonm predictions")
    logger.debug(f"Input position: {position}")
    logger.debug(f"Average Speeds: {avg_speeds}, seconds: {seconds}")
    logger.debug(f"Predicted Position: {proj_position}")

    return proj_position