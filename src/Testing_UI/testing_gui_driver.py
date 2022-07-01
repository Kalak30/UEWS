""" Starts and configures the Testing GUI application for UEWS
    Spawns an additional thread to handle UDP connection to UEWS Backend
"""

import os
import socket
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow

import proto_src.rsdf_pb2 as RsdfPB
from generated_ui.testing_ui import Ui_TestingServer





SENDER_THREAD = None

class SenderThread(QThread):
    """ A thread to send messages to the UEWS Backend
        Reads RSDF data in from a file and creates a UDP connection with the backend
        to send it data. Uses data interface defined in the proto_definitions/rsdf.proto file
    """
    msg_sent = pyqtSignal(str)
    time_d = 1 # Scroll bar cannot handle decimal, so use whole numbers and divide later
    reset_graph = False
    test_path = ""

    def restart(self):
        """ Starts the restart sequence for the sender thread
            This will tell the UEWS Backend that a restart is happening and
            will then begin reading the file again
        """
        self.reset_graph = True

    def set_test_file(self, test_file):
        """ Changes the path of the file being read. Test file should contain only
            RSDF data, otherwise errors may occur
        """
        self.test_path = test_file

    def set_time_dilation(self, factor: int):
        """ Sets the Time Dilation Factor. This value gets sent to the Backend so that it is aware
            Of the rate message should be coming in at.
        """
        self.time_d = 1/(factor/100)

    def run(self):
        """ Runs forever. Opens a file for reading and sends individual RSDF messages contained to
            the UEWS Backend.
            Creates a UDP connection and sends an RSDF protobuf defined in
            proto_definitions/rsdf.proto to the UEWS Backend. Once a message is sent, the QThread
            emits a msg_sent signal and the thread sleeps for 2 * time_dilation_factor seconds.
            The 2 seconds comes from the fact that RSDF data is sent at a very reliable period
            of 2 seconds.
        """
        # Run until server is dead
        while True:
            self.reset_graph = False
            # Open a specified file
            with open(self.test_path, encoding='utf-8') as f:
                total_message = ""
                sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
                while not self.reset_graph:
                    line = f.readline()
                    if not line:
                        break
                    total_message = total_message + line
                    if line[0:2] == "CS":
                        protobuf = RsdfPB.RSDF()
                        protobuf.raw_rsdf = total_message
                        protobuf.time_dilation = self.time_d
                        protobuf.reset = self.reset_graph
                        sock.sendto(protobuf.SerializeToString(), ('localhost', 6545))
                        self.msg_sent.emit(total_message)
                        total_message = ""
                        time.sleep(2* self.time_d)

# Must return the sender thread and maintain reference so it does not get garbage collected
def start_sending_thread(main_ui: Ui_TestingServer):
    """ Starts a thread that opens a file at a default path
        Connects signals from the ui to vital parts of the thread.
    """
    test_path = os.path.join("../../test_data/projection_test.txt")
    main_ui.selected_file.setText(test_path)

    thread = SenderThread()
    thread.test_path = test_path
    thread.start()
    thread.msg_sent.connect(main_ui.raw_rsdf.setText)
    main_ui.time_dilation_factor.valueChanged.connect(thread.set_time_dilation)
    main_ui.restart_button.clicked.connect(thread.restart)
    return thread

def init_file_dialog(main_ui: Ui_TestingServer):
    """ Initializes the File choosing dialog widget so different test files can be picked.
        A nested function is created to allow it to be called by a signal event.
        Connects to nested function to a signal event
    """
    def openFile():
        """ Creates a file dialog widget that opens a file.
            Changes the text box on the main ui describing the file chosen as well as chaning the
            test file of the sender thread if it is available.
        """
        options = QFileDialog.Options()
        test_path, _ = QFileDialog.getOpenFileName(main_ui.centralwidget, "Choose Test File", "",
                                                   "All Files(*);; Text Files (*.txt)",
                                                   options=options)
        if test_path:
            main_ui.selected_file.setText(test_path)
            if SENDER_THREAD:
                SENDER_THREAD.set_test_file(test_path)

    main_ui.OpenFileButton.clicked.connect(openFile)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    UEWS_Testing_GUI = QMainWindow()
    ui = Ui_TestingServer()
    ui.setupUi(UEWS_Testing_GUI)

    init_file_dialog(ui)
    SENDER_THREAD = start_sending_thread(ui)

    UEWS_Testing_GUI.show()
    sys.exit(app.exec_())
