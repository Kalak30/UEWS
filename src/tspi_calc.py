import math
from tspi import Vector
from statics import *


def get_delta(s1, s2, seconds):
    return (s1 - s2) / seconds


# Gets called upon creation and changing the pose of the record
def validate_pos(pos: Vector, knots):

    if pos.x < x_outlier["lower"] or pos.x > x_outlier["upper"] or pos.y < y_outlier["lower"] or \
            pos.y > y_outlier["upper"] or pos.z < z_outlier["lower"] or pos.z > z_outlier["upper"] or \
            knots > speed_outlier["upper"]:
        return False
    return True


# get my_speed in yards per second
def get_speed(my_speed, current_position, last_position, seconds):
    # alternatively this can be done by using the given my_speed and heading.
    print(current_position[0])
    print(last_position[0])
    # calculated my_speed in each direction with current and last positions (each position is in yards)
    print("seconds: ", seconds)
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

    print("xy_speed:     ", xy_speed)
    print("total speed: ", total_speed)

    # total_knots = totalSpeed * 0.592484
    total_knots = xy_speed * 0.592484

    # note: incoming knots only account for xy directions
    return total_knots


def get_time_diff(input_time, last_time):
    time_diff = input_time - last_time
    seconds = abs(time_diff.total_seconds())

    # Check if no time diff, avoids divide by zero error
    if seconds == 0:
        print("no time difference")
        seconds = 1000000

    return seconds
