import datetime
import numpy as np
from shapely.geometry import Point, Polygon
from multiprocessing.connection import Client
from multiprocessing.connection import Listener

import rsdf_parse
import tspi_calc
import tspi
from statics import *
import configurator


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
    config_args = configurator.get_config()
    # read in settings from config file?
    alerts = [np.empty(alertNum)]
    # alerts for current position (XYZ positions, depth violation).  Proj is same alerts but for projected position
    if alertType == 'consecutive':
        alerts = [np.zeros(alertNum, dtype=int)]
    elif alertType == 'cumulative':
        alerts = [np.zeros((alertNum, alertNumTotal), dtype=int)]

    print("alerts: ", alerts)


    # server
    address = ('', 5000)

    serv = Listener(address)
    while True:
        client = serv.accept()
        try:
            # Main loop
            while True:
                # received_data(client)
                msg = str(client.recv())
                print(msg)

                store = tspi.TSPIStore(ttl=5)
                # parse data
                new_record = rsdf_parse.parse_data(msg)
                # If new_record is pp : alert.pp_output()

                # If code 11 do the following
                store.add_record(new_record)
                # Reset alert_processor.no_sub_data_timer

                # Actual calculation stuff

        except EOFError as e:
            print("end of file")
            break


if __name__ == "__main__":
    main()
