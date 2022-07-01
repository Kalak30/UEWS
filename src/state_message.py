""" Wraps around the state protobuf generated class for ease of use.
"""
from google.protobuf import text_format

import proto_src.state_pb2 as StatePB

class StateMessage:
    """ A wrapper for the State protobuf. """
    def __init__(self, reset = False, raw_rsdf=""):
        self.protobuf = StatePB.State()
        self.protobuf.reset = reset
        self.protobuf.raw_rsdf = raw_rsdf
        
        # Initialize the store to have at least one record to avoid errors
        self.protobuf.store.records.append(StatePB.TSPIRecord())

    def set_valid_data(self, x_val=False, y_val=False, z_val=False, speed=False):
        """ Sets whether x,y,z,speed data is valid or not
        """
        self.protobuf.valid_x = x_val
        self.protobuf.valid_y = y_val
        self.protobuf.valid_z = z_val
        self.protobuf.valid_speed = speed

    def set_store(self, store):
        """ Because the store contains a list of Records, it must be copied from the other protobuf
        """
        self.protobuf.store.CopyFrom(store.toProtoBuf())

    def set_toggle_values(self, enough_valid=True, sub_in=True, proj_pos=True, 
                        send_warn=True, alarm_enable=True, alarm_on=True):
        """ Sets the values for true/false variables that aren't valid data"""
        self.protobuf.enough_valid_tracks = enough_valid
        self.protobuf.sub_in = sub_in
        self.protobuf.proj_pos_good = proj_pos
        self.protobuf.send_warn = send_warn
        self.protobuf.alarm_enable = alarm_enable
        self.protobuf.alarm_on = alarm_on

    def set_counters(self, depth_vio=0, total_alerts=0, no_sub=0, total_valid=0):
        """ Sets values of counter variables that keep track of things"""
        self.protobuf.depth_violations = depth_vio
        self.protobuf.total_alerts = total_alerts
        self.protobuf.no_sub = no_sub
        self.protobuf.total_valid_track = total_valid

    def set_reset(self, reset):
        """ Makes this state a reset
        """
        self.protobuf.reset = reset
    def set_rsdf(self, raw_rsdf):
        """ Sets the raw rsdf
        """
        self.protobuf.raw_rsdf = raw_rsdf
    def clear(self):
        """ Sets all values of the protobuf to default
        """
        self.protobuf.Clear()
    def serialize_to_string(self):
        """ Serializes the state so it can be transmistted
        """
        return self.protobuf.SerializeToString()

    def __str__(self):
        string = ""
        text_format.Parse(string, self)
        return string
