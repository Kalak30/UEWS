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


# needs updating
def alert_detector(current_position, last_position, current_time, last_time):
    return 0


# def setProjPosition(proj_pos, my_speed):
def main():
    config_args = configurator.get_config()

    # server
    address = ('', 5000)

    serv = Listener(address)
    while True:
        client = serv.accept()
        try:
            #create tspi store with specified time to live (ttl)
            store = tspi.TSPIStore(ttl=7)
            # Main loop
            while True:
                # received_data(client)
                msg = str(client.recv()) # Blocking
                print(msg)

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
