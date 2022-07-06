""" Helper functions and definitions to aid in connecting with other vital UEWS processes"""

# TODO: Turn this into a connection class
import socket
import threading
from dynaconf import settings

import state_message
import proto_src.gui_state_pb2 as GStatePB
import proto_src.gui_connection_pb2 as GConnPB

state_lock = threading.Lock()
class GUIPortHandler:
    """ Handles getting and initializing GUIPorts"""
    gui_port_list = []
    curr_index = 0
    def __init__(self):
        self.init_gui_ports()

    def init_gui_ports(self):
        """ Returns list of all GUI ports"""
        first=settings.GUI_PORT_RANGE["first"]
        last=settings.GUI_PORT_RANGE["last"]
        step=settings.GUI_PORT_RANGE["step"]
        self.gui_port_list =  [x for x in range(first, last, step)]

    def get_next(self):
        """ Gets the next available GUI port"""
        if self.curr_index >= len(self.gui_port_list):
            raise Exception("Tried to get a port, but no mroe are available")
        port = self.gui_port_list[self.curr_index]
        self.curr_index += 1
        return port

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
        data, self.remote_socket_address = self.socket.recvfrom(self.max_buff_size)
        if callback is None:
            return data, self.remote_socket_address
        
        return callback(data), self.remote_socket_address
    
    def send_back(self, msg):
        """ Sends a message back to the address last received from"""
        if self.remote_socket_address is None:
            return
        self.socket.sendto(msg, self.remote_socket_address)

    
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
GUI_EST_CONN = ('127.0.0.1', settings.GUI_EST_CONN_PORT)
GUI_STATE_RECV = ('127.0.0.1', settings.GUI_SERVICER_PORT)
GUI_STATE_SEND = (settings.RCO_GUI_IP, settings.RCO_GUI_PORT)
GUI_CONTROL_RECV = ('127.0.0.1', 9000)
class GUIConnection:
    """ Connects to a GUI. Handles threads associated with the connection"""
    gui_req_thread = None
    gui_control_thread = None
    def __init__(self, loc_state_recv, loc_control_recv, rem_state_recv, control_callback = None):
        
        self.state_conn = BidirectionalConnection(loc_recv=loc_state_recv,
                                                rem_recv=rem_state_recv)

        self.control_conn = ReceivingConnection(loc_soc_addr=loc_control_recv, rem_soc_addr=None)
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
            print(state_msg)
            self.state_conn.send(state_msg.serialize_to_string())

    def start_reception(self, state_msg):
        """ Starts threads to receive all async data. Does not include connection to server"""
        self.gui_req_thread = threading.Thread(target=self.await_gui_request,
                                               name="GUI_REQUEST_HANDLER", args=(state_msg, ))
        self.gui_req_thread.start()
        self.gui_control_thread = threading.Thread(target=self.await_gui_control,
                                               name="GUI_CONTROL_HANDLER")
        self.gui_control_thread.start()


def gui_control_callback(data):
    """ A callback for the GUI connection to handle gui_control messages"""
    gui_control = GStatePB.GUI_State()
    gui_control.ParseFromString(data)
    #AP.update(gui_control)
    #if hasattr(gui_control, "new_inhibit"):
    # then update new_inhibit
    return gui_control

def gui_establish_callback(data):
    """ A callback for the Establish Connection protobuf to handle a gui wanting to connect"""
    establish_connection = GConnPB.EstablishConnection()
    establish_connection.ParseFromString(data)
    return establish_connection.state_lis_port

class ConnectionHandler:
    """ Handles all connections for UEWS"""
    gui_connections = []
    def __init__(self, state_msg):
        self.server_conn = ReceivingConnection(loc_soc_addr=SERV_ADDRESS, rem_soc_addr=None)
        self.gui_conn_establish = ReceivingConnection(loc_soc_addr=GUI_EST_CONN, rem_soc_addr=None)
        self.gui_port_handle = GUIPortHandler()

        self.state_msg = state_msg
        self.gui_conn_est_thread = None
        
        self.listen_for_gui_connections()

    def await_gui_conn(self, state_msg):
        """ Waits for an establish connection from a GUI"""
        while True:
            state_lis_port, rem_addr = self.gui_conn_establish.recv(callback=gui_establish_callback)
            try:
                state_req_port = self.gui_port_handle.get_next()
                gui_state_port = self.gui_port_handle.get_next()
                establish_conn_ack = GConnPB.EstablishConnectionAck()

                establish_conn_ack.state_req_port = state_req_port
                establish_conn_ack.gui_state_port = gui_state_port
                self.gui_conn_establish.send_back(establish_conn_ack.SerializeToString())
                
                state_req = ('127.0.0.1', state_req_port)
                gui_state = ('127.0.0.1', gui_state_port)
                state_lis = (rem_addr[0], state_lis_port)
                self.gui_connections.append(GUIConnection(state_req, gui_state, state_lis))
                self.gui_connections[-1].start_reception(state_msg)
                
            except Exception as exception:
                print(f"Error: {exception}")
                exit()

    def listen_for_gui_connections(self):
        """ Creates a thread that will listen for guis attempting to connect to backend"""
        self.gui_conn_est_thread = threading.Thread(target= self.await_gui_conn, name="GUI_CONN",
                                                    args=(self.state_msg, ))
        self.gui_conn_est_thread.start()

    def send_reset(self, state_msg):
        """ Sends a reset message to all GUIs"""
        for gui_conn in self.gui_connections:
            gui_conn.send_reset(state_msg)
       

        

    

