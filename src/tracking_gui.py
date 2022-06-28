from cmath import e
from ctypes import alignment
from sre_parse import State
from tkinter import *
from random import randint
import logging

from pyparsing import col
import numpy as np
import statics
import calculation_state

from multiprocessing.connection import Connection, Listener

# These are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Places matplotlib plot on tkinter canvas
from matplotlib.figure import Figure    # For creating a figure
import time
import threading # Needed so that plot can update without freezing the GUI

logger = logging.getLogger(__name__)



class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title('UEWS Tracking GUI')
        self.resizable(0,0)
        self.rowconfigure(5, weight=2)
        self.fig = Figure()

        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.grid()

        self.state = None
        self.positions = np.zeros(shape=(1,2))
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        self.create_widgets()

        # Listen to backend
        address = ('localhost', 6000)
        listener = Listener(address)

        # Run state update in a different thread so that the GUI is still responsive
        threading.Thread(target=self.update_state, args=(listener,), daemon=True).start()

    
    def create_widgets(self):
        info_frame = Frame(self, borderwidth=10)

        # Creating Labels
        proj_x_lab = Label(info_frame, text="proj_x", anchor="e")
        proj_y_lab = Label(info_frame, text="proj_y", anchor="e")
        x_lab = Label(info_frame, text="x", anchor="e")
        y_lab = Label(info_frame, text="y", anchor="e")
        z_lab = Label(info_frame, text="z", anchor="e")
        course_lab = Label(info_frame, text="course", anchor="e")
        tp_course_lab = Label(info_frame, text="tp course", anchor="e")


        # Creating Info
        proj_x_info = Label(info_frame, text="px_info", width=20)
        proj_y_info = Label(info_frame, text="py_info", width=20)
        x_info = Label(info_frame, text="x_info", width=20)
        y_info = Label(info_frame, text="y_info", width=20)
        z_info = Label(info_frame, text="z_info", width=20)
        course_info = Label(info_frame, text="c_info", width=20)
        tp_course_info = Label(info_frame, text="tpc_info", width=20)
        
        

        # Placing Widgets
        proj_x_lab.grid(row=0,column=0, sticky='e')
        proj_x_info.grid(row=0, column=1, sticky='w')
        proj_y_lab.grid(row=1,column=0, sticky='e')
        proj_y_info.grid(row=1, column=1,sticky='w')

        course_lab.grid(row=3, column=0, sticky='e')
        course_info.grid(row=3, column=1, sticky='w')

        tp_course_lab.grid(row=4, column=0, sticky='e')
        tp_course_info.grid(row=4, column=1, sticky='w')

        x_lab.grid(row=0, column=2, sticky='e')
        y_lab.grid(row=1, column=2, sticky='e')
        z_lab.grid(row=2, column=2, sticky='e')

        x_info.grid(row=0, column=3, sticky='e')
        y_info.grid(row=1, column=3, sticky='e')
        z_info.grid(row=2, column=3, sticky='e')
        
        info_frame.pack(fill=BOTH, expand=True)
        self.graph.get_tk_widget().pack(fill=BOTH, expand=True)

    def plot(self):
        graph_height=3000
        graph_width=4000

        pos_list = []    
        center = 0
        self.ax.cla()
        self.ax.grid()

        if state is not None:
            pos_list = np.array([(record.position.x, record.position.y) for record in state.store.records])
            self.positions = np.vstack((self.positions, pos_list[0]))
            t_position = self.positions.T
            x_pos, y_pos = t_position
            self.ax.plot(x_pos, y_pos, color='green')
            center = pos_list[0]

        t_inner = np.array(statics.coords_inner).T
        t_center = np.array(statics.coords_center).T
        t_outer = np.array(statics.coords_outer).T

        x_inner, y_inner = t_inner
        x_center, y_center = t_center
        x_outer, y_outer = t_outer


        self.ax.plot(x_inner, y_inner, color='yellow')
        self.ax.plot(x_center, y_center, color='orange')
        self.ax.plot(x_outer, y_outer, color='red')

        self.ax.set_xlim(left=center[0]-graph_width/2, right=center[0]+graph_height/2)
        self.ax.set_ylim(bottom=center[1]-graph_height/2, top=center[1]+graph_height/2)
        

        self.ax.invert_xaxis()
        self.ax.invert_yaxis()
        
        

        self.graph.draw()
            
        
    def gui_handler(self):
        threading.Thread(target=self.plot, daemon=True).start()

    def update_state(self, listener):
        global state
        global new_data
        conn = listener.accept()
        while True:
            try:
                state = conn.recv()
                self.gui_handler()
            except EOFError as eof:
                logger.debug("End of File")
            
            print("new data")
            new_data = True

    
    


if __name__=="__main__":
    app = App()
    app.mainloop()