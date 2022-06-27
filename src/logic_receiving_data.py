import datetime
import numpy as np

from multiprocessing.connection import Client
from multiprocessing.connection import Listener

import rsdf_parse
import bounds_check
import tspi
from statics import *
import configurator


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
                if not bounds_check.in_bounds(new_record.position.x, new_record.position.y, new_record.position.z):
                    pass # Make an alert call

                # proj_pos = calc_pos(store) || proj_pos = store.calc_proj()
                # if not bounds_check.inbounds(proj_pos.x, proj_pos.y, proj_pos.z):
                #   Make an alert call
                
                

        except EOFError as e:
            print("end of file")
            break


if __name__ == "__main__":
    main()
