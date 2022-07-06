""" Wraps around the state protobuf generated class for ease of use. Also provides some dataclasses
    to make passing peices of state around
"""
from dataclasses import dataclass, field
from google.protobuf import text_format
import proto_src.state_pb2 as StatePB
from tspi import TSPIStore
from alert_processor import AlertProcessorState

@dataclass
class ValidationState:
    """ Stores state of how valid the position is"""
    valid_x: bool = field(default=False)
    valid_y: bool = field(default=False)
    valid_z: bool = field(default=False)
    valid_speed: bool = field(default=False)

    def full_valid(self):
        """ Returns true if the state if fully true"""
        return self.valid_x and self.valid_y and self.valid_z and self.valid_speed


@dataclass
class PositionsInBounds:
    """ Stores whether the current position (most recent record) is within bounds"""
    current: bool = field(default=False)
    projected: bool = field(default=False)


@dataclass
class StateMessage:
    """ A wrapper for the State protobuf. """
    protobuf: StatePB.State = field(default)

    def __post_init__(self):
        self.protobuf = StatePB.State()

    # Easiest way I have found to make other code clean an keep functionality of setting protobuf
    # values by just accessing the StateMessage object and not the protobuf directly
    @property
    def valid_x(self) -> bool:
        """ return valid x"""
        return self.protobuf.valid_x
    @valid_x.setter
    def valid_x(self, valid_x: bool) -> None:
        self.protobuf.valid_x = valid_x

    @property
    def valid_y(self) -> bool:
        """ return valid y"""
        return self.protobuf.valid_y
    @valid_y.setter
    def valid_y(self, valid_y: bool) -> None:
        self.protobuf.valid_y = valid_y

    @property
    def valid_z(self) -> bool:
        """ return valid z"""
        return self.protobuf.valid_z
    @valid_z.setter
    def valid_z(self, valid_z: bool) -> None:
        self.protobuf.valid_z = valid_z

    @property
    def valid_speed(self) -> bool:
        """ return valid z"""
        return self.protobuf.valid_speed
    @valid_speed.setter
    def valid_speed(self, valid_speed: bool) -> None:
        self.protobuf.valid_speed = valid_speed

    @property
    def enough_valid_tracks(self) -> bool:
        """ return enough_valid_tracks"""
        return self.protobuf.enough_valid_tracks
    @enough_valid_tracks.setter
    def enough_valid_tracks(self, evt: bool) -> None:
        self.protobuf.enough_valid_tracks = evt
    
    @property
    def sub_in(self) -> bool:
        """ return sub_in"""
        return self.protobuf.sub_in
    @sub_in.setter
    def sub_in(self, sub_in: bool) -> None:
        self.protobuf.sub_in = sub_in

    @property
    def proj_pos_good(self) -> bool:
        """ return proj_pos_good"""
        return self.protobuf.proj_pos_good
    @proj_pos_good.setter
    def proj_pos_good(self, ppg: bool) -> None:
        self.protobuf.proj_pos_good = ppg

    @property
    def send_warn(self) -> bool:
        """ return send_warn"""
        return self.protobuf.send_warn
    @send_warn.setter
    def send_warn(self, send_warn: bool) -> None:
        self.protobuf.send_warn = send_warn
    
    @property
    def alarm_enable(self) -> bool:
        """ return alarm_enable"""
        return self.protobuf.alarm_enable
    @alarm_enable.setter
    def alarm_enable(self, alarm_enable: bool) -> None:
        self.protobuf.alarm_enable = alarm_enable

    @property
    def alarm_on(self) -> bool:
        """ return alarm_on"""
        return self.protobuf.alarm_on
    @alarm_on.setter
    def alarm_on(self, alarm_on: bool) -> None:
        self.protobuf.alarm_on = alarm_on

    @property
    def depth_violations(self) -> bool:
        """ return depth_violations"""
        return self.protobuf.depth_violations
    @depth_violations.setter
    def depth_violations(self, depth_violations: int) -> None:
        self.protobuf.depth_violations = depth_violations

    @property
    def total_alerts(self) -> bool:
        """ return total_alerts"""
        return self.protobuf.total_alerts
    @total_alerts.setter
    def total_alerts(self, total_alerts: int) -> None:
        self.protobuf.total_alerts = total_alerts

    @property
    def no_sub(self) -> bool:
        """ return no_sub"""
        return self.protobuf.no_sub
    @no_sub.setter
    def no_sub(self, no_sub: int) -> None:
        self.protobuf.no_sub = no_sub

    @property
    def total_valid_track(self) -> bool:
        """ return total_valid_track"""
        return self.protobuf.total_valid_track
    @total_valid_track.setter
    def total_valid_track(self, total_valid_track: int) -> None:
        self.protobuf.total_valid_track = total_valid_track

    @property
    def reset(self) -> bool:
        """ return reset"""
        return self.protobuf.reset
    @reset.setter
    def reset(self, reset: int) -> None:
        self.protobuf.reset = reset

    @property
    def raw_rsdf(self) -> bool:
        """ return raw_rsdf"""
        return self.protobuf.raw_rsdf
    @raw_rsdf.setter
    def raw_rsdf(self, raw_rsdf: str) -> None:
        self.protobuf.raw_rsdf = raw_rsdf

    @property
    def store(self) -> bool:
        """ return store"""
        return self.protobuf.store
    @store.setter
    def store(self, store: TSPIStore) -> None:
        self.protobuf.store.CopyFrom(store.toProtoBuf())

    @property
    def seconds_alarm(self) -> bool:
        """ return seconds_alarm"""
        return self.protobuf.seconds_alarm
    @seconds_alarm.setter
    def seconds_alarm(self, seconds: int) -> None:
        self.protobuf.seconds_alarm = seconds

    @property
    def auto_alarm(self) -> bool:
        """ return auto_alarm"""
        return self.protobuf.auto_alarm
    @auto_alarm.setter
    def auto_alarm(self, auto_alarm: bool) -> None:
        self.protobuf.auto_alarm = auto_alarm

    @property
    def manual_alarm(self) -> bool:
        """ return manual_alarm"""
        return self.protobuf.manual_alarm
    @manual_alarm.setter
    def manual_alarm(self, manual_alarm: bool) -> None:
        self.protobuf.manual_alarm = manual_alarm

    def set_validation_state(self, v_state: ValidationState):
        """ Updates the validation state variables based on a validation state"""
        self.valid_x = v_state.valid_x
        self.valid_y = v_state.valid_y
        self.valid_z = v_state.valid_z
        self.valid_speed = v_state.valid_speed

    def set_positions_in_bounds(self, pbounds: PositionsInBounds):
        """ Updates the good positions values based on a PostiionsInBounds object"""
        self.sub_in = pbounds.current
        self.proj_pos_good = pbounds.projected

    def set_ap_state(self, ap_state: AlertProcessorState):
        """ Sets alert processor state values based on an alertprocessor state object"""
        self.enough_valid_tracks = ap_state.consec_valid == 0
        self.send_warn = False
        self.alarm_enable = ap_state.alarm_enable
        self.alarm_on = False
        self.depth_violations = ap_state.depth_violations
        self.total_alerts = ap_state.total_alert
        self.no_sub = ap_state.total_no_sub
        self.total_valid_track = ap_state.total_valid_track

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
