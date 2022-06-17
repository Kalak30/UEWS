import datetime
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


# config file variables
# alertType = 'consecutive'  # or 'cumulative'
alertType = 'cumulative'
alertNum = 3
alertNumTotal = 5  # only used for cumulative (i.e. 3 out of past 5)


# needs updating
def alert_detector(current_position, last_position, current_time, last_time):
    return 0


# def setProjPosition(proj_pos, my_speed):
def main():
    # read in settings from config file?
    alerts = [np.empty(alertNum)]
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
