
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from multiprocessing.connection import Listener

import logging


class ReceiverThread(QThread):
    new_state = pyqtSignal(object)
    # TODO: Make address configurable
    def run(self):
        self.address = ('localhost', 6000)
        self.listener = Listener(self.address)
        while True:
            conn = self.listener.accept()
            try:
                state = conn.recv()
            except EOFError as eof:
                logging.debug("End of File")
            else:
                self.new_state.emit(state)
            finally:
                conn.close()
    

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
        self.receiver_thread = ReceiverThread(self)
        self.receiver_thread.start()
        self.receiver_thread.new_state.connect(self.evt_new_state)


    def evt_new_state(self, state):
        print("newState")
        print(state)
        self.receivedState.emit(state)

        # Extract Values
        latest_record = state.store.records[0]
        valid_data = state.valid_data
        alarm_data = state.alarm_data
        counters = state.counters

        x = latest_record.position.x
        y = latest_record.position.y
        z = latest_record.position.z
        proj_x = latest_record.proj_position.x
        proj_y = latest_record.proj_position.y
        course = latest_record.heading

        tp_course = course-11.3
        if tp_course < 0:
            tp_course += 360

        speed = latest_record.knots

        valid_track_pts = counters["total_valid_track"]
        no_sub_count = counters["total_no_sub"]
        alert_count = counters["total_alert"]
        depth_violations = counters["depth_violations"]

        x_ok = valid_data["x"]
        y_ok = valid_data["y"]
        z_ok = valid_data["z"]
        speed_ok = valid_data["speed"]

        valid_consec = alarm_data["5_valid"]
        sub_in = alarm_data["sub_in"]
        proj_pos_good = alarm_data["proj_pos_good"]
        sub_pos_good = alarm_data["sub_pos_good"]
        send_warn = alarm_data["send_warn"]
        alarm_enable = alarm_data["alarm_enable"]
        alarm_on = alarm_data["alarm_on"]

        # Emit Values
        self.set_x.emit(x)
        self.set_y.emit(y)
        self.set_z.emit(z)
        self.set_proj_x.emit(proj_x)
        self.set_proj_y.emit(proj_y)
        self.set_course.emit(course)
        self.set_tp_course.emit(tp_course)

        self.set_speed.emit(speed)
        self.set_valid_track_pts.emit(valid_track_pts)
        self.set_no_sub_data.emit(no_sub_count)
        self.set_alert_count.emit(alert_count)
        self.set_depth_violations.emit(depth_violations)

        self.set_x_ok.emit(x_ok)
        self.set_y_ok.emit(y_ok)
        self.set_z_ok.emit(z_ok)
        self.set_speed_ok.emit(speed_ok)
        
        self.set_valid_consec_track.emit(valid_consec)
        self.set_sub_in_bounds.emit(sub_in)
        self.set_proj_pos_good.emit(proj_pos_good)
        self.set_sub_pos_good.emit(sub_pos_good)
        self.set_send_warn_tones.emit(send_warn)
        self.set_alarm_enable.emit(alarm_enable)
        self.set_alarm_on.emit(alarm_on)
            