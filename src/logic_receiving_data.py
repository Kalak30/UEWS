""" Receives data from server, does calculation and verification, then
    sends data to GUIs
"""

import logging
import logging.config
from os import path
from dynaconf import settings


import proto_src.rsdf_pb2 as RsdfPB
import statics
from connection_handle import ConnectionHandler, state_lock
import rsdf_parse
import bounds_check
from tspi import TSPIRecord, TSPIStore
import tspi
from alert_processor import AlertProcessorState, AlertProcessor
from state_message import ValidationState, PositionsInBounds, StateMessage


logging.config.fileConfig(path.join(path.dirname(path.abspath('')), statics.LOGGER_CONFIG_PATH))
logger = logging.getLogger(__name__)


def do_validation(new_record: TSPIRecord):
    """ Does validation process and returns a tuple of 4 bools
        (valid_x, valid_y, valid_z, valid_speed)
    """
    valid_x = bounds_check.check_x(new_record.position.x)
    valid_y = bounds_check.check_y(new_record.position.y)
    valid_z = bounds_check.check_z(new_record.position.z)
    valid_speed = bounds_check.check_speed(new_record.knots)
    return ValidationState(valid_x, valid_y, valid_z, valid_speed)

def check_bounds_and_alert(new_record: TSPIRecord, store: TSPIStore,
                           alert_p: AlertProcessor):
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

    return PositionsInBounds(current=pos_good, projected=proj_pos_good)


def update_state(state_msg: StateMessage, store: TSPIStore=None, msg:RsdfPB.RSDF=None,
                 validation: ValidationState=None, ap_state: AlertProcessorState=None,
                 good_positions: PositionsInBounds=None):
    """ Updates the values within the StateMessage object"""

    with state_lock:
        state_msg.clear()
        state_msg.reset = msg.reset
        state_msg.raw_rsdf = msg.raw_rsdf
        state_msg.store = store
        state_msg.set_validation_state(validation)
        state_msg.set_positions_in_bounds(good_positions)
        state_msg.set_ap_state(ap_state)

# def setProjPosition(proj_pos, my_speed):
def main():
    """ Main loop of the backend data processing loop. """
    alert_p = AlertProcessor()
    state_msg = StateMessage()

    connection_handle = ConnectionHandler(state_msg=state_msg)

    #create tspi store with specified time to live (ttl)
    store = tspi.TSPIStore(ttl=settings.TSPI_TTL)

    while True:
        msg = RsdfPB.RSDF()
        data, _ = connection_handle.server_conn.recv()
        msg.ParseFromString(data)

        if msg.reset:
            connection_handle.send_reset(state_msg=state_msg)
        else:
            # If new data set starts with no pp, will not get reset
            state_msg.reset = False

        # parse raw rsdf from server
        new_record = rsdf_parse.parse_data(msg.raw_rsdf)

        validation = ValidationState()
        good_positions = PositionsInBounds()

        if new_record is None:
            alert_p.recived_no_code11_data(store.get_newest_record())

        else:
            #reset sub timer
            alert_p.recived_all_data()

            # Validate incoming data
            validation = do_validation(new_record)

            if validation.full_valid():
                store.add_record(new_record)
                alert_p.valid_data()
            else:
                alert_p.invalid_data()

            good_positions = check_bounds_and_alert(new_record, store, alert_p)


        # Create and send state to GUI client
        ap_state = alert_p.get_alarm_state()
        update_state(state_msg, store, msg, validation, ap_state, good_positions)
        #new_record.print_values()

if __name__ == "__main__":
    main()
