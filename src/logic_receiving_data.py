
import time
import numpy as np

import socket


import proto_src.rsdf_pb2 as RsdfPB
import rsdf_parse
import bounds_check
import tspi
from statics import *
import configurator
import alert_processor
import logging
import bounds_check
import state_message

logger = logging.getLogger(__name__)
max_buff_size = 1024

# def setProjPosition(proj_pos, my_speed):
def main():
    print("in main")
    config_args = configurator.get_config()
    custom_proj = False
    AP = alert_processor.AlertProcessor()


    # Both connections should end up being closed at some point
    # server
    serv_address = ('', 6545)
    serv_socket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
    serv_socket.bind(serv_address)

    #create tspi store with specified time to live (ttl)
    store = tspi.TSPIStore(ttl=7)

    while True:
        # received_data(client)
        msg = RsdfPB.RSDF()
        data, addr = serv_socket.recvfrom(max_buff_size) # Blocking
        msg.ParseFromString(data)
        

        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        StateMsg = state_message.StateMessage(reset=True)
        if msg.reset:
            sock.sendto(StateMsg.SerializeToString(),('localhost', 6000))
        
        # parse data
        new_record = rsdf_parse.parse_data(msg.raw_rsdf)

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
        ap_state = AP.get_alarm_state()

        StateMsg = state_message.StateMessage(reset=msg.reset, raw_rsdf=msg.raw_rsdf)
        StateMsg.setValidData(valid_x, valid_y, valid_z, valid_speed)
        StateMsg.setStore(store)
        StateMsg.setToggleValues(enough_valid=ap_state["consec_valid"]==0, sub_in=pos_good,
                                    proj_pos=proj_pos_good, send_warn=False, alarm_enable=ap_state["alarm_enable"],
                                    alarm_on=False)
        StateMsg.setCounters(depth_vio=ap_state["depth_violations"], total_alerts=ap_state["total_alert"],
                                no_sub=ap_state["total_no_sub"], total_valid=ap_state["total_valid_track"])
        

        
        sock.sendto(StateMsg.SerializeToString(), ('localhost', 6000))

        new_record.print_values()

if __name__ == "__main__":
    main()
