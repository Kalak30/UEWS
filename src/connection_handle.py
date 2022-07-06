""" Helper functions and definitions to aid in connecting with other vital UEWS processes"""

# TODO: Turn this into a connection class
import socket
import threading
from dynaconf import settings

import state_message
import proto_src.gui_state_pb2 as GStatePB

state_lock = threading.Lock()
class Connection:
    """ Represents a connection between two processes"""
    def __init__(self, loc_soc_addr, rem_soc_addr, conn_type=socket.SOCK_DGRAM):
        self.local_socket_address = loc_soc_addr
        self.remote_socket_address = rem_soc_addr
        self.conn_type = conn_type
        self.max_buff_size=1024

class ReceivingConnection(Connection):
    """ Handler for creating a socket to connect and receive data"""
    def __init__(self, loc_soc_addr, rem_soc_addr, conn_type=socket.SOCK_DGRAM):
        Connection.__init__(self,  loc_soc_addr, rem_soc_addr, conn_type)
        self.socket = socket.socket(family=socket.AF_INET, type=self.conn_type)
        self.socket.bind(self.local_socket_address)

    def recv(self, callback=None):
        """ Returns data if no callback supplied. Otherwise returns result of callback"""
        data, _ = self.socket.recvfrom(self.max_buff_size)
        if callback is None:
            return data
        
        return callback(data)
    
class SendingConnection(Connection):
    """ Handler for creating a socket to connect and send data"""
    def __init__(self, loc_soc_addr, rem_soc_addr, conn_type=socket.SOCK_DGRAM):
        Connection.__init__(self,  loc_soc_addr, rem_soc_addr, conn_type)
        self.socket = socket.socket(family=socket.AF_INET, type=self.conn_type)
    
    def send(self, message):
        """ Sends message to remote address"""
        self.socket.sendto(message, self.remote_socket_address)
    

class BidirectionalConnection:
    """ A Bidirectional Connection. Can both send and receive as it has two sockets"""
    def __init__(self, loc_recv, rem_recv, rem_send=None, loc_send=None,
                 recv_conn_type=socket.SOCK_DGRAM, send_conn_type=socket.SOCK_DGRAM):
                 self.recv_conn = ReceivingConnection(loc_recv, rem_send, recv_conn_type)
                 self.send_conn = SendingConnection(loc_send, rem_recv, send_conn_type)
    
    def recv(self, callback=None):
        """ Calls recv from the recv connection object. Blocks"""
        self.recv_conn.recv(callback=callback)
    
    def send(self, message):
        """ Sends a message to remote send address"""
        self.send_conn.send(message)


SERV_ADDRESS = (settings.SERVER_IP, settings.SERVER_PORT)
GUI_STATE_RECV = ('127.0.0.1', settings.GUI_SERVICER_PORT)
GUI_STATE_SEND = (settings.RCO_GUI_IP, settings.RCO_GUI_PORT)
GUI_CONTROL_RECV = ('127.0.0.1', 9000)
class GUIConnection:
    """ Connects to a GUI"""
    def __init__(self, control_callback = None):
        self.state_conn = BidirectionalConnection(loc_recv=GUI_STATE_RECV,
                                                rem_recv=GUI_STATE_SEND)

        self.control_conn = ReceivingConnection(loc_soc_addr=GUI_CONTROL_RECV, rem_soc_addr=None)
        self.control_callback = control_callback

    def await_gui_request(self, state_msg: state_message.StateMessage):
        """ Waits for a request from the GUI so the current state can be sent"""
        while True:
            self.state_conn.recv()
            self.state_conn.send(state_msg.serialize_to_string())
    
    def await_gui_control(self):
        """ Waits for the GUI to send control information"""
        while True:
            # Add some callback function that takes raw protobuf
            self.control_conn.recv(callback=self.control_callback)

    def send_reset(self, state_msg: state_message.StateMessage):
        """ Sends a reset message so the GUI can clean its interface"""
        with state_lock:
            state_msg.clear()
            state_msg.reset = True
            self.state_conn.send(state_msg.serialize_to_string())

    def send_state(self,state_msg: state_message.StateMessage):
        """ Sends the current STATE_MSG to the socket_addr. Ensures that no data is updated in the
            middle of transmission
        """
        with state_lock:
            self.state_conn.send(state_msg.serialize_to_string())


def gui_control_callback(data):
    """ A callback for the GUI connection to handle gui_control messages"""
    gui_control = GStatePB.GUI_State()
    gui_control.ParseFromString(data)
    #AP.update(gui_control)
    #if hasattr(gui_control, "new_inhibit"):
    # then update new_inhibit
    return gui_control

class ConnectionHandler:
    """ Handles all connections for UEWS"""
    def __init__(self, state_msg):
        self.server_conn = ReceivingConnection(loc_soc_addr=SERV_ADDRESS, rem_soc_addr=None)
        self.gui_conn = GUIConnection(control_callback=gui_control_callback)
        self.gui_req_thread = None
        self.gui_control_thread = None
        self.start_reception(state_msg=state_msg)

    def start_reception(self, state_msg):
        """ Starts threads to receive all async data. Does not include connection to server"""
        self.gui_req_thread = threading.Thread(target=self.gui_conn.await_gui_request, 
                                               name="RCO_GUI_REQUEST_HANDLER", args=(state_msg, ))
        self.gui_req_thread.start()
        self.gui_control_thread = threading.Thread(target=self.gui_conn.await_gui_control,
                                               name="RCO_GUI_CONTROL_HANDLER")
        self.gui_control_thread.start()

    

