from doctest import testfile
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
senderThread = None

class SenderThread(QThread):
    msg_sent = pyqtSignal(str)
    close_connection = False
    time_d = 1 # Scroll bar cannot handle decimal, so use whole numbers and divide later
    test_path = ""

    def restart(self):
        self.close_connection = True
        while not self.isFinished():
            continue
        self.quit()
        self.start()

    def setTestFile(self, test_file):
        self.test_path = test_file

    def setTimeDilation(self, factor: int):
        self.time_d = 1/(factor/100)

    def run(self):
        self.close_connection = False
        with open(self.test_path) as f:
            print(self.test_path)
            total_message = ""
            c  = self.establishConn(('localhost', 6545))
            while not self.close_connection:
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

# Must return the sender thread and maintain reference so it does not get garbage collected
def start_sending_thread(ui: Ui_TestingServer):
    test_path = os.path.join(current_dir, "../../test_data/projection_test.txt")
    ui.selected_file.setText(test_path)

    thread = SenderThread()
    thread.test_path = test_path
    thread.start()
    thread.msg_sent.connect(ui.raw_rsdf.setText)
    ui.time_dilation_factor.valueChanged.connect(thread.setTimeDilation)
    ui.restart_button.clicked.connect(thread.restart)
    return thread

def init_file_dialog(ui: Ui_TestingServer):
    def openFile():
        options = QFileDialog.Options()
        test_path, _ = QFileDialog.getOpenFileName(ui.centralwidget, "Choose Test File", "", "All Files(*);; Text Files (*.txt)", options=options)
        if test_path:
            ui.selected_file.setText(test_path)
            if senderThread:
                senderThread.setTestFile(test_path)

    ui.OpenFileButton.clicked.connect(openFile)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    UEWS_Testing_GUI = QMainWindow()
    ui = Ui_TestingServer()
    ui.setupUi(UEWS_Testing_GUI)

    init_file_dialog(ui)
    senderThread = start_sending_thread(ui)
    
    UEWS_Testing_GUI.show()
    sys.exit(app.exec_())