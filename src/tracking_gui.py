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
        self.proj_position = np.zeros(shape=(1,2))
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        self.top_frame = Frame(self, borderwidth=10)
        self.create_widgets()

        # Listen to backend
        address = ('localhost', 6000)
        listener = Listener(address)

        # Run state update in a different thread so that the GUI is still responsive
        threading.Thread(target=self.update_state, args=(listener,), daemon=True).start()

    
    def create_widgets(self):
        info_frame = self.top_frame

        # Creating Labels
        Label(info_frame, text="proj_x", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=0,column=0, sticky='e')
        Label(info_frame, text="proj_y", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=1,column=0, sticky='e')
        Label(info_frame, text="x", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=0, column=2, sticky='e')
        Label(info_frame, text="y", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=1, column=2, sticky='e')
        Label(info_frame, text="z", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=2, column=2, sticky='e')
        Label(info_frame, text="course", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=3, column=0, sticky='e')
        Label(info_frame, text="tp course", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=4, column=0, sticky='e')
        Label(info_frame, text="speed", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=4, column=2, sticky='e')

        Label(info_frame, text="x ok", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=0, column=5, sticky='w')
        Label(info_frame, text="y ok", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=1, column=5, sticky='w')
        Label(info_frame, text="z ok", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=2, column=5, sticky='w')
        Label(info_frame, text="speed ok", anchor="e", width=10,
              borderwidth=3, relief="ridge").grid(row=4, column=5, sticky='w')

        


        # Creating Info
        Label(info_frame, text="px_info", width=10, name="proj_x_info").grid(row=0, column=1, sticky='w')
        Label(info_frame, text="py_info", width=10, name="proj_y_info").grid(row=1, column=1,sticky='w')
        Label(info_frame, text="x_info", width=10, name="x_info").grid(row=0, column=3, sticky='w')
        Label(info_frame, text="y_info", width=10, name="y_info").grid(row=1, column=3, sticky='w')
        Label(info_frame, text="z_info", width=10, name="z_info").grid(row=2, column=3, sticky='w')
        Label(info_frame, text="c_info", width=10, name="course_info").grid(row=3, column=1, sticky='w')
        Label(info_frame, text="tpc_info", width=10, name="tp_course_info").grid(row=4, column=1, sticky='w')
        Label(info_frame, text="speed_info", width=10, name="speed_info").grid(row=4, column=3, sticky='w')

        Label(info_frame, text="", width=5, height=2, name="x_ok_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=0, column=4, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="y_ok_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=1, column=4, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="z_ok_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=2, column=4, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="speed_ok_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=4, column=4, sticky='e')

        
        info_frame.pack(fill=BOTH, expand=True)
        self.graph.get_tk_widget().pack(fill=BOTH, expand=True)

        
    def plot(self):
        graph_height=3000
        graph_width=4000

        pos_list_max = 200
        proj_pos_list_max = 20

        center = 0
        self.ax.cla()
        self.ax.grid()

        if state is not None:
            # Get new positions and projected positions. This does not look through the store to see if there is anything we have missed
            new_record = state.store.records[0]
            new_pos = np.array((new_record.position.x, new_record.position.y))
            new_proj_pos = np.array((new_record.proj_position.x, new_record.proj_position.y))

            self.positions = np.vstack((self.positions, new_pos))
            if len(self.positions) > pos_list_max:
                np.delete(self.positions, (0), axis=0)

            self.proj_position = np.vstack((self.proj_position, new_proj_pos))
            if len(self.proj_position) > proj_pos_list_max:
                np.delete(self.proj_position, (0), axis=0)

            t_position = self.positions.T
            t_proj_pos = self.proj_position.T
            x_pos, y_pos = t_position
            proj_x, proj_y = t_proj_pos

            self.ax.plot(x_pos, y_pos, color='green')
            self.ax.plot(proj_x, proj_y, color='red')
            center = new_pos

            # Update all info widgets
            
            child_widgets = self.top_frame.winfo_children()
            # TODO: Is there some way to do this with a function / callback maybe
            for child_widget in child_widgets:
                if child_widget.winfo_name() == 'proj_x_info':
                    child_widget.configure(text=str("{:.1f}").format(new_record.proj_position.x))
                elif child_widget.winfo_name() == 'proj_y_info':
                    child_widget.configure(text=str("{:.1f}").format(new_record.proj_position.y))
                elif child_widget.winfo_name() == 'x_info':
                    child_widget.configure(text=str("{:.1f}").format(new_record.position.x))
                elif child_widget.winfo_name() == 'y_info':
                    child_widget.configure(text=str("{:.1f}").format(new_record.position.y))
                elif child_widget.winfo_name() == 'z_info':
                    child_widget.configure(text=str("{:.1f}").format(new_record.position.z))
                elif child_widget.winfo_name() == 'course_info':
                    child_widget.configure(text=str("{:.1f}").format(new_record.heading))
                elif child_widget.winfo_name() == 'speed_info':
                    child_widget.configure(text=str("{:.1f}").format(new_record.knots))
                elif child_widget.winfo_name() == "x_ok_info":
                    if state.valid_data["x"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "y_ok_info":
                    if state.valid_data["y"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "z_ok_info":
                    if state.valid_data["z"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "speed_ok_info":
                    if state.valid_data["speed"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")


        t_inner = np.array(statics.coords_inner).T
        t_center = np.array(statics.coords_center).T
        t_outer = np.array(statics.coords_outer).T

        x_inner, y_inner = t_inner
        x_center, y_center = t_center
        x_outer, y_outer = t_outer


        self.ax.plot(x_inner, y_inner, color='orange')
        self.ax.plot(x_center, y_center, color='yellow')
        self.ax.plot(x_outer, y_outer, color='green')

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
                if type(state) is not calculation_state.CalculationState:
                    logger.error("Received something that was not a state object")
                else:
                    self.gui_handler()
            except EOFError as eof:
                logger.debug("End of File")
            
            new_data = True

    
    


if __name__=="__main__":
    app = App()
    app.mainloop()