import datetime
import numpy as np

from multiprocessing.connection import Client
from multiprocessing.connection import Listener

import rsdf_parse
import tspi_calc
import tspi
from statics import *
import configurator
import alert_processor
import logging

logger = logging.getLogger(__name__)

# needs updating
def alert_detector(current_position, last_position, current_time, last_time):
    return 0


# def setProjPosition(proj_pos, my_speed):
def main():
    print("in main")
    config_args = configurator.get_config()
    alert_process = alert_processor.AlertProcessor()

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
<<<<<<< HEAD
                msg = str(client.recv())
                #print(msg)
=======
                msg = str(client.recv()) # Blocking
                print(msg)
>>>>>>> 3fae0971e804bcb62b5d6827c60c9492794c38d8

                #message recived, rest pp timer
                

                try:
                
                    # parse data
                    new_record = rsdf_parse.parse_data(msg)

                    #reset sub timer
                    alert_process.recived_all_data()

                    #store record
                    store.add_record(new_record)

                    #check new data bounds

                #no code 11, don't add records
                except Exception as e: #TODO some better way to do this??
                    alert_process.recived_noCode11_data()
                    logger.debug(e)


                # Actual calculation stuff

        except EOFError as e:
            print("end of file")
            break


if __name__ == "__main__":
    main()
