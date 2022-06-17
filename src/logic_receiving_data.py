import datetime
import math
import numpy as np
from shapely.geometry import Point, Polygon
from multiprocessing.connection import Client
from multiprocessing.connection import Listener

import rsdf_parse

# border boundaries - in yards
# These may be stored in some file in the future, so it is easier for them to change
chords_inner = [(2500, -1200), (2500, 1000), (3100, 1500), (5900, 1500), (8500, 1500), (10000, 1200), (12100, 870),
                (14050, 600), (15560, 1100), (15560, -1530), (9000, -1530), (6800, -830), (5800, -680), (5200, -720),
                (2500, -1200)]
chords_center = [(2500, -1230), (2500, 1220), (3100, 1680), (5900, 1530), (8500, 1590), (10000, 1220), (12100, 930),
                 (14050, 1250), (15560, 1500), (15560, -1680), (9000, -1680), (6800, -900), (5800, -800), (5200, -810),
                 (2500, -1230)]
chords_outer = [(2500, -1400), (2500, 1900), (3100, 1900), (5900, 1600), (8500, 1740), (10000, 1300), (12100, 1150),
                (14050, 1350), (15560, 1500), (15560, -1900), (9000, -1900), (6800, -1020), (5800, -970), (5200, -933),
                (2500, -1400)]

inner_poly = Polygon(chords_inner)


# needs updating
def alert_detector(current_position, last_position, current_time, last_time):
    return 0;


# get my_speed in yards per second
def get_speed(my_speed, current_position, last_position, seconds):
    # alternatively this can be done by using the given my_speed and heading.
    print(current_position[0])
    print(last_position[0])
    # calculated my_speed in each direction with current and last positions (each position is in yards)
    print("seconds: ", seconds)
    my_speed[0] = (current_position[0] - last_position[0]) / seconds;
    my_speed[1] = (current_position[1] - last_position[1]) / seconds;
    my_speed[2] = (current_position[2] - last_position[2]) / seconds;


# calculate speed in x and y direction from the given knots and heading values
def get_speed_from_knots(given_speed, my_knots, heading):
    # rotate 90 so that head is degrees off of x-axis (instead of y-axis) ((or y instead of x, not sure))
    heading = heading - 90
    # print("incoming knots : ",my_knots,"incoming heading: ",heading)
    given_speed[0] = (1.68781 * (my_knots * math.sin((math.radians(heading)))))
    given_speed[1] = (1.68781 * (my_knots * math.cos((math.radians(heading)))))


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


# config file variables
alertType = 'consecutive'  # or 'cumulative'
alertType = 'cumulative'
alertNum = 3
alertNumTotal = 5  # only used for cumulative (i.e. 3 out of past 5)


# def setProjPosition(proj_pos, my_speed):
def main():
    # read in settings from config file?

    # alerts for current position (XYZ positions, depth violation).  Proj is same alerts but for projected position
    if alertType == 'consecutive':
        alerts = [np.zeros(alertNum, dtype=int)]
    elif alertType == 'cumulative':
        alerts = [np.zeros(alertNum, alertNumTotal)]

    print("alerts: ", alerts)

    proj_alerts = [0, 0]

    # input data (x,y,z,knot,head)
    input_position = [0, 0, 0, 0, 0]

    # input time
    input_time = datetime.datetime(1, 1, 1, 1, 1, 1)

    # last input time
    last_time = datetime.datetime(1, 1, 1, 1, 1, 1)

    # server
    address = ('', 5000)

    serv = Listener(address)
    while True:
        client = serv.accept()
        try:
            while True:
                # received_data(client)
                msg = str(client.recv())
                print(msg)

                # parse data
                r = rsdf_parse.parse_data(msg, input_position, input_time,
                                          last_time)  # if return 3 (no pp) reset last position?

        except EOFError as e:
            print("end of file")
            break


if __name__ == "__main__":
    main()
