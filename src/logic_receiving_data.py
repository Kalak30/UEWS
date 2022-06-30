
import time
import numpy as np

from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from multiprocessing.pool import ThreadPool

import threading
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

def getClientConn(address):

    tr_conn = None

    try:
        tr_conn = Client(address)
    except ConnectionRefusedError as e:
        logger.exception("Connection to Tracking GUI failed because connection was refused. Trying again")
    except:
        logger.exception("Connection to Tracking GUI threw unkown exception")
    
    return tr_conn

# def setProjPosition(proj_pos, my_speed):
def main():
    print("in main")
    config_args = configurator.get_config()
    custom_proj = False
    AP = alert_processor.AlertProcessor()


    # Both connections should end up being closed at some point
    # server
    serv_address = ('', 6545)
    serv = Listener(serv_address)

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

                #message recived, rest pp timer
                

                #------TODO make this a functin?--------
                
                # parse data
                new_record = rsdf_parse.parse_data(msg)

                if(new_record == None):
                    AP.recived_noCode11_data()
                    continue

                #reset sub timer
                AP.recived_all_data()

                # Validate incoming data
                valid_x = bounds_check.check_x(new_record.position.x)
                valid_y = bounds_check.check_y(new_record.position.y)
                valid_z = bounds_check.check_z(new_record.position.z)
                valid_speed = bounds_check.check_speed(new_record.knots)

                if valid_x and valid_y and valid_z and valid_speed:
                    store.add_record(new_record)
                    AP.valid_data()
                else:
                    AP.invalid_data()
                    
                pos_good = True
                proj_pos_good = True
                # Check current pos is in
                if not bounds_check.in_bounds(new_record.position):
                    pos_good = False
                
                #check depth
                if(bounds_check.check_in_depth(new_record.position.z)):
                    AP.depth_ok()
                else:
                    AP.depth_violation()

                store.get_prediction(new_record, custom_proj)

                # Check projected pos in
                if not bounds_check.in_bounds(new_record.proj_position):
                    proj_pos_good = False
                

                if proj_pos_good and pos_good:
                    AP.bounds_ok()
                else:
                    AP.bounds_violation()
                    

                 # Create and send state to GUI client
                valid_data = {"x": valid_x, "y": valid_y, "z": valid_z, "speed": valid_speed}
                ap_state = AP.get_alarm_state()

                alarm_data = {"5_valid": (ap_state["consec_valid"] == 0), "sub_in": pos_good, 
                              "proj_pos_good": proj_pos_good, "sub_pos_good": valid_x and valid_y and valid_z and valid_speed,
                              "send_warn": False, "alarm_enable": ap_state["alarm_enable"], "alarm_on": False}

                counters = {"depth_violations": ap_state["depth_violations"], "total_alert": ap_state["total_alert"], 
                            "total_no_sub": ap_state["total_no_sub"], "total_valid_track": ap_state["total_valid_track"]}
                            
                state = calculation_state.CalculationState(reset=False, store=store,  raw_rsdf=msg, valid_data = valid_data, 
                                                           alarm_data=alarm_data, counters=counters)

                # Tracking GUI Connect
                tr_address = ('localhost', 6000)
                tr_conn = getClientConn(tr_address)

                if tr_conn is not None:
                    # Send the state and close
                    tr_conn.send(state)
                    tr_conn.close()


                new_record.print_values()


        except EOFError as e:
            print("end of file")
            state = calculation_state.CalculationState(reset=True, store=None, raw_rsdf=None, valid_data=None,
                                                       alarm_data=None, counters=None)
            tr_address = ('localhost', 6000)
            tr_conn = getClientConn(tr_address)
            if tr_conn is not None:
                    # Send the state and close
                    tr_conn.send(state)
                    tr_conn.close()


            


if __name__ == "__main__":
    main()
