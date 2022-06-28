from asyncio.windows_events import NULL
import datetime
from tabnanny import check
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

logger = logging.getLogger(__name__)

# needs updating
def alert_detector(current_position, last_position, current_time, last_time):
    return 0


# def setProjPosition(proj_pos, my_speed):
def main():
    print("in main")
    config_args = configurator.get_config()
    AP = alert_processor.AlertProcessor()

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
                #print(msg)

                #message recived, rest pp timer
                

                #------TODO make this a functin?--------
                
                # parse data
                new_record = rsdf_parse.parse_data(msg)

                if(new_record == NULL):
                    AP.recived_noCode11_data()
                    continue

                #reset sub timer
                AP.recived_all_data()

                #check data in record (if not vailid aka false, don't store)
                if(bounds_check.check_vaild_record(new_record.position, new_record.knots)):
                    store.add_record(new_record)
                    AP.valid_data()
                    
                else:
                    AP.invalid_data()
                    
                #check depth
                if(bounds_check.check_in_depth(new_record.position.z)):
                    AP.depth_ok()
                else:
                    AP.depth_violation()

                #TODO cehck boundary projections
                if(bounds_check.check_project_boundary(new_record.proj_position)):
                    AP.bounds_violation()
                else:
                    AP.bounds_ok()

                new_record.print_values()


        except EOFError as e:
            print("end of file")
            break


if __name__ == "__main__":
    main()
