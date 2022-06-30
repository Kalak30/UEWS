import tspi
import proto_src.state_pb2 as StatePB

class StateMessage:
    def __init__(self, reset = False, raw_rsdf=""):
        self.protobuf = StatePB.State()
        self.protobuf.reset = reset
        self.protobuf.raw_rsdf = raw_rsdf

    def setValidData(self, x=0, y=0, z=0, speed=0):
        self.protobuf.valid_x = x
        self.protobuf.valid_y = y
        self.protobuf.valid_z = z
        self.valid_speed = speed

    def setStore(self, store):
        self.protobuf.store.CopyFrom(store.toProtoBuf())
    
    def setToggleValues(self, enough_valid=True, sub_in=True, proj_pos=True, 
                        send_warn=True, alarm_enable=True, alarm_on=True):
        self.protobuf.enough_valid_tracks = enough_valid
        self.protobuf.sub_in = sub_in
        self.protobuf.proj_pos_good = proj_pos
        self.protobuf.send_warn = send_warn
        self.protobuf.alarm_enable = alarm_enable
        self.protobuf.alarm_on = alarm_on
    
    def setCounters(self, depth_vio=0, total_alerts=0, no_sub=0, total_valid=0):
        self.protobuf.depth_violations = depth_vio
        self.protobuf.total_alerts = total_alerts
        self.protobuf.no_sub = no_sub
        self.protobuf.total_valid_track = total_valid

    def SerializeToString(self):
        return self.protobuf.SerializeToString()