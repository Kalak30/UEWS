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

<<<<<<< HEAD
                #no code 11, don't add records
                except Exception as e: #TODO some better way to do this??
                    alert_process.recived_noCode11_data()
                    logger.debug(e)


                # Actual calculation stuff
                if not bounds_check.in_bounds(new_record.position.x, new_record.position.y, new_record.position.z):
                    pass # Make an alert call

                # proj_pos = calc_pos(store) || proj_pos = store.calc_proj()
                # if not bounds_check.inbounds(proj_pos.x, proj_pos.y, proj_pos.z):
                #   Make an alert call
                
                
=======
>>>>>>> alarm_processor

        except EOFError as e:
            print("end of file")
            break


if __name__ == "__main__":
    main()
