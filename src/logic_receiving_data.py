
import time
import numpy as np

from multiprocessing.connection import Client
from multiprocessing.connection import Listener

import rsdf_parse
import bounds_check
import tspi
from statics import *
import configurator
import alert_processor
import logging
import bounds_check
import calculation_state

logger = logging.getLogger(__name__)

# needs updating
def alert_detector(current_position, last_position, current_time, last_time):
    return 0


# def setProjPosition(proj_pos, my_speed):
def main():
    print("in main")
    config_args = configurator.get_config()
    custom_proj = False
    AP = alert_processor.AlertProcessor()


    # Both connections should end up being closed at some point
    # server
    serv_address = ('', 5000)
    serv = Listener(serv_address)

    # Tracking GUI
    tr_address = ('localhost', 6000)
    tr_conn = None
    while tr_conn is None:
        try:
            tr_conn = Client(tr_address)
        except ConnectionRefusedError as e:
            time.sleep(1) # Wait a bit for other processes to start
            continue

        
    while True:
        client = serv.accept()
        try:
            #create tspi store with specified time to live (ttl)
            store = tspi.TSPIStore(ttl=7)
            # Main loop
            while True:
                # received_data(client)
                msg = str(client.recv()) # Blocking
                #print(msg)

                #message recived, rest pp timer
                

                #------TODO make this a functin?--------
                
                # parse data
                new_record = rsdf_parse.parse_data(msg)

                if(new_record == None):
                    AP.recived_noCode11_data()
                    continue

                #reset sub timer
                AP.recived_all_data()

                valid_x = bounds_check.check_x(new_record.position.x)
                valid_y = bounds_check.check_y(new_record.position.y)
                valid_z = bounds_check.check_z(new_record.position.z)
                valid_speed = bounds_check.check_speed(new_record.knots)

                if valid_x and valid_y and valid_z and valid_speed:
                    store.add_record(new_record)
                    AP.valid_data()
                else:
                    AP.invalid_data()
                    
                #check depth
                if(bounds_check.check_in_depth(new_record.position.z)):
                    AP.depth_ok()
                else:
                    AP.depth_violation()

                #get projections
                store.get_prediction(new_record, custom_proj)
                
                valid_data = {"x": valid_x, "y": valid_y, "z": valid_z, "speed": valid_speed}
                state = calculation_state.CalculationState(store, msg, valid_data)

                
                tr_conn.send(state)
                #TODO cehck boundary projections
                if(bounds_check.in_bounds(new_record.proj_position)):
                    AP.bounds_violation()
                else:
                    AP.bounds_ok()

                new_record.print_values()


        except EOFError as e:
            print("end of file")
            break


if __name__ == "__main__":
    main()
