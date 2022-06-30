from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from multiprocessing.connection import Client
import time
import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(current_dir))

from generated_ui.testing_ui import Ui_TestingServer

test_path = os.path.join(current_dir, "../../test_data/projection_test.txt")
print(test_path)



class SenderThread(QThread):
    msg_sent = pyqtSignal(str)
    time_d = 1 # Scroll bar cannot handle decimal, so use whole numbers and divide later

    def setTimeDilation(self, factor: int):
        self.time_d = 1/(factor/100)

    def run(self):
        with open(test_path) as f:
            total_message = ""
            c  = self.establishConn(('localhost', 6545))
            while True:
                line = f.readline()
                if not line: 
                    break
                #print(line)  \
                #try parsing by checksum
                #print("\n", line[0:2], "\n")
                total_message = total_message + line
                #print("message so far: ", total_message)
                if (line[0:2] == "CS"):
                    print("end of message, sending")
                    c.send(total_message)
                   
                    self.msg_sent.emit(total_message)
                    total_message = ""
                    time.sleep(2* self.time_d)
            c.close()
        
    def establishConn(self, address):
        # Establish a connection
        connected = False
        while not connected:
            try:
                c = Client(address)
                connected = True
            except ConnectionRefusedError as e:
                print("Connection Failed")
        return c

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    UEWS_Testing_GUI = QMainWindow()
    ui = Ui_TestingServer()
    ui.setupUi(UEWS_Testing_GUI)

    senderThread = SenderThread()
    senderThread.start()
    senderThread.msg_sent.connect(ui.raw_rsdf.setText)
    ui.time_dilation_factor.valueChanged.connect(senderThread.setTimeDilation)

    UEWS_Testing_GUI.show()
    sys.exit(app.exec_())