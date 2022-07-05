""" Receives data from server, does calculation and verification, then
    sends data to GUIs
"""

import logging
import logging.config
import threading
from os import path
from dynaconf import settings


import proto_src.rsdf_pb2 as RsdfPB
import statics
from connection_handle import *
import rsdf_parse
import bounds_check
from tspi import TSPIRecord, TSPIStore
import tspi
import alert_processor
import state_message


logging.config.fileConfig(path.join(path.dirname(path.abspath('')), statics.LOGGER_CONFIG_PATH))
logger = logging.getLogger(__name__)

GUI_SOCKET = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
GUI_SERVICER_SOCKET = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
SERVER_SOCKET = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)

def do_validation(new_record: TSPIRecord):
    """ Does validation process and returns a tuple of 4 bools
        (valid_x, valid_y, valid_z, valid_speed)
    """
    valid_x = bounds_check.check_x(new_record.position.x)
    valid_y = bounds_check.check_y(new_record.position.y)
    valid_z = bounds_check.check_z(new_record.position.z)
    valid_speed = bounds_check.check_speed(new_record.knots)
    return valid_x, valid_y, valid_z, valid_speed

def check_bounds_and_alert(new_record: TSPIRecord, store: TSPIStore,
                           alert_p: alert_processor.AlertProcessor):
    """ Checks if the new record is in bounds and if the projected position of that record is 
        in bounds. Also checks for depth violation of the new record.
        If there is an issue with any of these, then a signal is sent to the alert processor
        Returns a dictionary containing whether the current and projected positions are good
        keys = {"current", "projected"}
    """
    custom_proj = False
    pos_good = True
    proj_pos_good = True
    # Check current pos is in
    if not bounds_check.in_bounds(new_record.position):
        pos_good = False

    #check depth
    if bounds_check.check_in_depth(new_record.position.z):
        alert_p.depth_ok()
    else:
        alert_p.depth_violation()

    store.get_prediction(new_record, custom_proj)

    # Check projected pos in
    if not bounds_check.in_bounds(new_record.proj_position):
        proj_pos_good = False


    if proj_pos_good and pos_good:
        alert_p.bounds_ok()
    else:
        alert_p.bounds_violation()

    return {"current": pos_good, "projected": proj_pos_good}


def update_state(state_msg, store: TSPIStore, msg:RsdfPB.RSDF,
                 validation, ap_state, good_positions):
    """ Updates the values within the StateMessage object"""
    with state_lock:
        state_msg.clear()
        state_msg.set_reset(msg.reset)
        state_msg.set_rsdf(msg.raw_rsdf)
        state_msg.set_valid_data(
                                validation["valid_x"],
                                validation["valid_y"],
                                validation["valid_z"],
                                validation["valid_speed"]
                                )                 
        state_msg.set_store(store)
        state_msg.set_toggle_values(enough_valid=ap_state["consec_valid"]==0,
                                    sub_in=good_positions["current"],
                                    proj_pos=good_positions["projected"],
                                    send_warn=False,
                                    alarm_enable=ap_state["alarm_enable"],
                                    alarm_on=False)
        state_msg.set_counters(depth_vio=ap_state["depth_violations"],
                                total_alerts=ap_state["total_alert"],
                                no_sub=ap_state["total_no_sub"],
                                total_valid=ap_state["total_valid_track"]
                                )

# def setProjPosition(proj_pos, my_speed):
def main():
    """ Main loop of the backend data processing loop. """
    alert_p = alert_processor.AlertProcessor()
    state_msg = state_message.StateMessage()

    setup_sockets(SERVER_SOCKET, GUI_SERVICER_SOCKET)

    gui_handler = threading.Thread(target=await_gui_request, name="RCO_GUI_REQUEST_HANDLER",
                     args=(GUI_SERVICER_SOCKET, state_msg))

    gui_handler.start()

    #create tspi store with specified time to live (ttl)
    store = tspi.TSPIStore(ttl=settings.TSPI_TTL)

    while True:
        msg = RsdfPB.RSDF()
        data = receive_from_server(SERVER_SOCKET)
        msg.ParseFromString(data)

        if msg.reset:
            send_reset(GUI_SOCKET_ADDRESS, GUI_SOCKET, state_msg)

        # parse raw rsdf from server
        new_record = rsdf_parse.parse_data(msg.raw_rsdf)

        if new_record is None:
            alert_p.recived_no_code11_data(store.get_newest_record())
            continue

        #reset sub timer
        alert_p.recived_all_data()

        # Validate incoming data
        valid_x, valid_y, valid_z, valid_speed = do_validation(new_record)
        validation = {
                      "valid_x": valid_x,
                      "valid_y": valid_y,
                      "valid_z": valid_z,
                      "valid_speed": valid_speed
                      }

        # Get a variable to tell if everything is valid
        fully_valid = True
        for value in validation.items():
            fully_valid &= value[1]

        if fully_valid:
            store.add_record(new_record)
            alert_p.valid_data()
        else:
            alert_p.invalid_data()

        good_positions = check_bounds_and_alert(new_record, store, alert_p)


        # Create and send state to GUI client
        ap_state = alert_p.get_alarm_state()
        update_state(state_msg, store, msg, validation, ap_state, good_positions)
        new_record.print_values()

if __name__ == "__main__":
    main()
