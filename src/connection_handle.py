""" Helper functions and definitions to aid in connecting with other vital UEWS processes"""

# TODO: Turn this into a connection class
import socket
import threading
from dynaconf import settings

import state_message
import proto_src.gui_state_pb2 as GStatePB

MAX_BUFF_SIZE = 1024
SERV_ADDRESS = (settings.SERVER_IP, settings.SERVER_PORT)
GUI_SERVICER_ADDRESS = ('127.0.0.1', settings.GUI_SERVICER_PORT)

GUI_SOCKET_ADDRESS = (settings.RCO_GUI_IP, settings.RCO_GUI_PORT)

state_lock = threading.Lock()

def setup_sockets(server_socket,  gui_servicer_socket):
    """ Binds the listening sockets """
    server_socket.bind(SERV_ADDRESS)
    gui_servicer_socket.bind(GUI_SERVICER_ADDRESS)

def update_gui_data(gui_data):
    """ Updates alarm processor with information from GUI"""
    gstate = GStatePB.GUI_State()
    gstate.ParseFromString(gui_data)

def send_reset(gui_socket_addr, gui_socket: socket.socket, state_msg: state_message.StateMessage):
    """ Sends a reset message so the GUI can clean its interface"""
    with state_lock:
        state_msg.clear()
        state_msg.set_reset(True)
        gui_socket.sendto(state_msg.serialize_to_string(), gui_socket_addr)


def await_gui_request(gui_socket: socket.socket, state_msg: state_message.StateMessage):
    """ Waits for a request from the GUI so the current state can be sent"""
    while True:
        gui_data, _ = gui_socket.recvfrom(MAX_BUFF_SIZE)
        update_gui_data(gui_data)
        send_state(GUI_SOCKET_ADDRESS, gui_socket, state_msg)

def send_state(socket_addr, gui_socket: socket.socket, state_msg: state_message.StateMessage):
    """ Sends the current STATE_MSG to the socket_addr. Ensures that no data is updated in the
        middle of transmission
    """
    with state_lock:
        gui_socket.sendto(state_msg.serialize_to_string(), socket_addr)

def receive_from_server(server_socket: socket.socket):
    """Receives message from server and return raw data"""
    data, _ = server_socket.recvfrom(MAX_BUFF_SIZE)
    return data
