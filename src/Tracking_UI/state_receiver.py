
import socket
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget
from dynaconf import settings
from google.protobuf.text_format import MessageToString

import proto_src.state_pb2 as StatePB
import proto_src.gui_state_pb2 as GStatePB

# TODO: Make address configurable
LISTENING_SOCKET_ADDR = ('127.0.0.1', settings.RCO_GUI_PORT)
BACK_STATE_RECV = ('127.0.0.1', settings.GUI_SERVICER_PORT)
BACK_CONTROL_RECV = ('127.0.0.1', 9000)

LOCAL_RECV =  socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
LOCAL_SEND = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

class SendingThread(QThread):
    """ Thread to send messages to the backend requesting updates"""
    state_req = GStatePB.StateRequest()
    gui_state = GStatePB.GUI_State()

    def auto_alarm(self, auto_alarm):
        """ Updates the auto_alarm value in the GUI state protobuf"""
        self.gui_state.auto_alarm = auto_alarm
        self.send_control_update()

    def new_inhibit(self, new_inhibit):
        """ Sets the new_inhibit alarm value in the GUI state protobuf"""
        self.gui_state.new_inhibit = new_inhibit
        self.send_control_update()

    def manual_pressed(self, manual_pressed):
        """ Sets whether the manual override button has been pressed in the last cycle"""
        self.gui_state.manual_pressed = manual_pressed
        self.send_control_update()

    def run(self):
        """ Continually sends to the backend"""
        be_socket = LOCAL_SEND
        while True:
            be_socket.sendto(self.state_req.SerializeToString(), BACK_STATE_RECV)
            time.sleep(0.1)

    def send_control_update(self):
        """ Sends a message to backend indicating that gui control has changed"""
        be_socket = LOCAL_SEND
        be_socket.sendto(self.gui_state.SerializeToString(), BACK_CONTROL_RECV)
        self.gui_state.clear()




class ReceiverThread(QThread):
    """ Thread to receive state information from the backend"""
    new_state = pyqtSignal(object)
    max_buff_size = 1024

    def run(self):
        """ Connects to the backend and emits a new_state notice"""
        sock = LOCAL_RECV
        sock.bind(LISTENING_SOCKET_ADDR)
        state = StatePB.State()
        prev_recv = StatePB.State()
        while True:
            data, _ = sock.recvfrom(self.max_buff_size)
            state.ParseFromString(data)
            self.emit_signal(state, prev_recv)
            # Simply assigning state to prev_recv is bad as it is a reference,
            prev_recv.ParseFromString(data)

            
        

    def emit_signal(self, state, prev_recv):
        """ Checks if there is duplicate data, emits if there is"""

        if prev_recv is None or state.reset is True:
            self.new_state.emit(state)
            return

        # Completely the same, no need to emit signals
        if MessageToString(prev_recv) == MessageToString(state):
            return

        if len(state.store.records) == 0 or len(prev_recv.store.records) == 0:
            return

        new_record = state.store.records[0]
        old_record = prev_recv.store.records[0]
        
        
        # Only update graph on change in position
        if old_record.x != new_record.x or old_record.y != new_record.y or \
            old_record.proj_x != new_record.proj_x or \
            old_record.proj_y != new_record.proj_y:
            self.new_state.emit(state)



class StateReceiver(QWidget):
    """Receives Messages from backend
    """
    receivedState = pyqtSignal(object, name="receivedState")

    set_proj_x = pyqtSignal(int)
    set_proj_y = pyqtSignal(int)
    set_course = pyqtSignal(int)
    set_tp_course = pyqtSignal(int)
    set_x = pyqtSignal(int)
    set_y = pyqtSignal(int)
    set_z = pyqtSignal(int)
    set_speed = pyqtSignal(int)
    set_valid_track_pts = pyqtSignal(int)
    set_no_sub_data = pyqtSignal(int)
    set_alert_count = pyqtSignal(int)
    set_depth_violations = pyqtSignal(int)

    set_x_ok = pyqtSignal(bool)
    set_y_ok = pyqtSignal(bool)
    set_z_ok = pyqtSignal(bool)
    set_speed_ok = pyqtSignal(bool)
    set_valid_consec_track = pyqtSignal(bool)
    set_sub_in_bounds = pyqtSignal(bool)
    set_proj_pos_good = pyqtSignal(bool)
    set_sub_pos_good = pyqtSignal(bool)
    set_send_warn_tones = pyqtSignal(bool)
    set_alarm_enable = pyqtSignal(bool)
    set_alarm_on = pyqtSignal(bool)

    set_on_colour = pyqtSignal(int)
    set_off_colour = pyqtSignal(int)
    set_shape = pyqtSignal(int)


    def __init__(self, *args, **kwargs):
        super(StateReceiver, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.set_on_colour.emit(2)
        self.set_off_colour.emit(1)
        self.run()

    def run(self):
        """ Starts a receiver and sender thread connecting them to slots"""
        self.receiver_thread = ReceiverThread(self)
        self.sender_thread = SendingThread(self)

        self.receiver_thread.start()
        self.sender_thread.start()

        self.receiver_thread.new_state.connect(self.evt_new_state)


    def evt_new_state(self, state):
        """ Extract values from received event and emits signals to the rest of the gui"""
        self.receivedState.emit(state)

        if len(state.store.records) == 0:
            return
        
        latest_record = state.store.records[0]

        # Emit Values
        self.set_x.emit(latest_record.x)
        self.set_y.emit(latest_record.y)
        self.set_z.emit(latest_record.z)
        self.set_proj_x.emit(latest_record.proj_x)
        self.set_proj_y.emit(latest_record.proj_y)
        self.set_course.emit(latest_record.course)

        tp_course = latest_record.course-11.3
        if tp_course < 0:
            tp_course += 360

        self.set_tp_course.emit(tp_course)

        self.set_speed.emit(latest_record.speed)
        self.set_valid_track_pts.emit(state.total_valid_track)
        self.set_no_sub_data.emit(state.no_sub)
        self.set_alert_count.emit(state.total_alerts)
        self.set_depth_violations.emit(state.depth_violations)

        self.set_x_ok.emit(state.valid_x)
        self.set_y_ok.emit(state.valid_y)
        self.set_z_ok.emit(state.valid_z)
        self.set_speed_ok.emit(state.valid_speed)
        self.set_valid_consec_track.emit(state.enough_valid_tracks)
        self.set_sub_in_bounds.emit(state.sub_in)
        self.set_proj_pos_good.emit(state.proj_pos_good)

        sub_pos_good = state.valid_x and state.valid_y and state.valid_z and state.valid_speed
        self.set_sub_pos_good.emit(sub_pos_good)

        self.set_send_warn_tones.emit(state.send_warn)
        self.set_alarm_enable.emit(state.alarm_enable)
        self.set_alarm_on.emit(state.alarm_on)

    def auto_alarm(self, auto_alarm):
        """ Updates the auto_alarm value in the GUI state protobuf"""
        self.sender_thread.auto_alarm(auto_alarm)

    def new_inhibit(self, new_inhibit):
        """ Sets the new_inhibit alarm value in the GUI state protobuf"""
        self.sender_thread.new_inhibit(new_inhibit)

    def manual_pressed(self, manual_pressed):
        """ Sets whether the manual override button has been pressed in the last cycle"""
        self.sender_thread.manual_pressed(manual_pressed)
            