from tkinter import *
import logging

from pyparsing import col
import numpy as np
import statics
import calculation_state

from multiprocessing.connection import Connection, Listener

# These are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Places matplotlib plot on tkinter canvas
from matplotlib.figure import Figure    # For creating a figure
from matplotlib.ticker import MultipleLocator
import threading # Needed so that plot can update without freezing the GUI

logging.basicConfig(level=logging.DEBUG)



class App(Tk):
    def __init__(self):
        super().__init__()
        #self.geometry("1000x700")
        self.title('UEWS Tracking GUI')
        self.state('zoomed')
        #self.resizable(0,0)
        self.rowconfigure(5, weight=2)
        self.fig = Figure()

        # Configuring the Axes Object for plotting sub track
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        x_ml = MultipleLocator(50)
        y_ml = MultipleLocator(50)
        self.ax.xaxis.set_minor_locator(x_ml)
        self.ax.yaxis.set_minor_locator(y_ml)
        self.ax.grid(which='major', color='b', linestyle='-', linewidth=1)
        self.ax.xaxis.grid(which='minor', color='b', linestyle=':', linewidth=0.7)
        self.ax.yaxis.grid(which='minor', color='b', linestyle=':', linewidth=0.7)
        self.ax.set_facecolor((0,0,0,1))


        self.state = None
        self.positions = np.empty(shape=(1,2))
        self.proj_positions = self.positions
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

        self.proj_x_val = StringVar(info_frame,"0")
        self.proj_y_val = StringVar(info_frame,"0")
        self.course_val = StringVar(info_frame,"0")
        self.tp_course_val = StringVar(info_frame,"0")
        self.x_val = StringVar(info_frame,"0")
        self.y_val = StringVar(info_frame,"0")
        self.z_val = StringVar(info_frame,"0")
        self.speed_val = StringVar(info_frame,"0")
        self.valid_tracks_val = StringVar(info_frame, "0")
        self.no_sub_data_val = StringVar(info_frame, "0")
        self.alert_count_val = StringVar(info_frame, "0")
        self.depth_violation_val = StringVar(info_frame, "0")


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

        Label(info_frame, text="x ok", anchor="w", width=10, padx=2,
              borderwidth=3, relief="ridge").grid(row=0, column=5, sticky='w')
        Label(info_frame, text="y ok", anchor="w", width=10, padx=2,
              borderwidth=3, relief="ridge").grid(row=1, column=5, sticky='w')
        Label(info_frame, text="z ok", anchor="w", width=10, padx=2,
              borderwidth=3, relief="ridge").grid(row=2, column=5, sticky='w')
        Label(info_frame, text="speed ok", anchor="w", width=10, padx=2,
              borderwidth=3, relief="ridge").grid(row=4, column=5, sticky='w')

        Label(info_frame, text="5 valid consec trk pts", anchor="e", width=10, wraplength=65, padx=2,
              borderwidth=3, relief="ridge").grid(row=0, column=7, sticky='w')
        Label(info_frame, text="Sub in bounds", anchor="e", width=10, wraplength= 65, padx=2,
              borderwidth=3, relief="ridge").grid(row=1, column=7, sticky='w')
        Label(info_frame, text="Projected pos good", anchor="e", width=10, wraplength=65, padx=2,
              borderwidth=3, relief="ridge").grid(row=2, column=7, sticky='w')
        Label(info_frame, text="sub pos good", anchor="e", width=10, wraplength=65, padx=2,
              borderwidth=3, relief="ridge").grid(row=4, column=7, sticky='w')

        Label(info_frame, text="Send Warning Tones", anchor="e", width=10, wraplength=65, padx=2,
              borderwidth=3, relief="ridge").grid(row=0, column=9, sticky='w')
        Label(info_frame, text="Alarm Enable", anchor="e", width=10, wraplength= 65, padx=2,
              borderwidth=3, relief="ridge").grid(row=1, column=9, sticky='w')
        Label(info_frame, text="Alarm On", anchor="e", width=10, wraplength=65, padx=2,
              borderwidth=3, relief="ridge").grid(row=2, column=9, sticky='w')

        Label(info_frame, text="Valid Track Pts", anchor="e", width=15,
              borderwidth=3, relief="ridge").grid(row=0,column=10, sticky='e')
        Label(info_frame, text="No Sub Data", anchor="e", width=15,
              borderwidth=3, relief="ridge").grid(row=1,column=10, sticky='e')
        Label(info_frame, text="Alert Count", anchor="e", width=15,
              borderwidth=3, relief="ridge").grid(row=2, column=10, sticky='e')
        Label(info_frame, text="Depth Violations", anchor="e", width=15,
              borderwidth=3, relief="ridge").grid(row=3, column=10, sticky='e')
        


        # Creating Info
        Label(info_frame, textvariable=self.proj_x_val, width=10).grid(row=0, column=1, sticky='w')
        Label(info_frame, textvariable=self.proj_y_val, width=10).grid(row=1, column=1,sticky='w')
        Label(info_frame, textvariable=self.x_val, width=10).grid(row=0, column=3, sticky='w')
        Label(info_frame, textvariable=self.y_val, width=10).grid(row=1, column=3, sticky='w')
        Label(info_frame, textvariable=self.z_val, width=10).grid(row=2, column=3, sticky='w')
        Label(info_frame, textvariable=self.course_val, width=10).grid(row=3, column=1, sticky='w')
        Label(info_frame, textvariable=self.tp_course_val, width=10).grid(row=4, column=1, sticky='w')
        Label(info_frame, textvariable=self.speed_val, width=10).grid(row=4, column=3, sticky='w')

        Label(info_frame, textvariable=self.valid_tracks_val, width=10).grid(row=0, column=11, sticky='w')
        Label(info_frame, textvariable=self.no_sub_data_val, width=10).grid(row=1, column=11, sticky='w')
        Label(info_frame, textvariable=self.alert_count_val, width=10).grid(row=2, column=11, sticky='w')
        Label(info_frame, textvariable=self.depth_violation_val, width=10).grid(row=3, column=11, sticky='w')

        Label(info_frame, text="", width=5, height=2, name="x_ok_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=0, column=4, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="y_ok_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=1, column=4, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="z_ok_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=2, column=4, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="speed_ok_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=4, column=4, sticky='e')

        Label(info_frame, text="", width=5, height=2, name="5_consec_trk_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=0, column=6, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="sub_in_bounds_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=1, column=6, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="proj_pos_good_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=2, column=6, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="sub_pos_good_info", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=4, column=6, sticky='e')

        Label(info_frame, text="", width=5, height=2, name="send_warn", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=0, column=8, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="alarm_enable", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=1, column=8, sticky='e')
        Label(info_frame, text="", width=5, height=2, name="alarm_on", pady=1,
              borderwidth=2, relief="groove", bg="gray").grid(row=2, column=8, sticky='e')

        
        info_frame.pack(fill=BOTH, expand=True)
        self.graph.get_tk_widget().pack(fill=BOTH, expand=True)

        
    def plot(self):
        graph_height=3000
        graph_width=4000
        pos_list_max = 200
        proj_pos_list_max = 20
        center = 0

        # Clean the graph
        for artist in self.ax.lines + self.ax.collections:
            artist.remove()
        

        if state is not None:
            # Get new positions and projected positions. This does not look through the store to see if there is anything we have missed
            new_record = state.store.records[0]
            new_pos = np.array((new_record.position.x, new_record.position.y))
            new_proj_pos = np.array((new_record.proj_position.x, new_record.proj_position.y))
            logging.debug("=======")
            logging.debug("new state")
            logging.debug(f"new_pos: {new_pos}")
            logging.debug(f"new_proj_pos: {new_proj_pos}")
            

            self.positions = np.vstack((self.positions, new_pos))
            if len(self.positions) > pos_list_max:
                self.positions = np.delete(self.positions, (0), axis=0)

            self.proj_positions = np.vstack((self.proj_positions, new_proj_pos))
            if len(self.proj_positions) > proj_pos_list_max:
                self.proj_positions = np.delete(self.proj_positions, (0), axis=0)

            t_position = self.positions.T
            t_proj_pos = self.proj_positions.T
            x_pos, y_pos = t_position
            proj_x, proj_y = t_proj_pos

            self.ax.plot(x_pos, y_pos, color='green')
            self.ax.plot(proj_x, proj_y, color='red')
            center = new_pos

            # Update all info widgets
            course = new_record.heading
            tp_course = course-11.3
            if tp_course < 0:
                tp_course += 360

            self.proj_x_val.set(str("{:.1f}").format(new_record.proj_position.x))
            self.proj_y_val.set(str("{:.1f}").format(new_record.proj_position.y))
            self.x_val.set(str("{:.1f}").format(new_record.position.x))
            self.y_val.set(str("{:.1f}").format(new_record.position.y))
            self.z_val.set(str("{:.1f}").format(new_record.position.z))
            self.course_val.set(str("{:.1f}").format(course))
            self.tp_course_val.set(str("{:.1f}").format(tp_course))
            self.speed_val.set(str("{:.1f}").format(new_record.knots))

            self.valid_tracks_val.set(str(state.counters["total_valid_track"]))
            self.no_sub_data_val.set(str(state.counters["total_no_sub"]))
            self.alert_count_val.set(str(state.counters["total_alert"]))
            self.depth_violation_val.set(str(state.counters["depth_violations"]))

            
            child_widgets = self.top_frame.winfo_children()
            logging.debug(f"alarm_data: {state.alarm_data}")
            logging.debug(f"valid_data: {state.valid_data}")
            logging.debug(f"coutners: {state.counters}")
            # TODO: Is there some way to do this with a function / callback maybe
            
            for child_widget in child_widgets:
                if child_widget.winfo_name() == "x_ok_info":
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

                elif child_widget.winfo_name() == "5_consec_trk_info":
                    if state.alarm_data["5_valid"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "sub_in_bounds_info":
                    if state.alarm_data["sub_in"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "proj_pos_good_info":
                    if state.alarm_data["proj_pos_good"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "sub_pos_good_info":
                    if state.alarm_data["sub_pos_good"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "send_warn":
                    if state.alarm_data["send_warn"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "alarm_enable":
                    if state.alarm_data["alarm_enable"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")
                elif child_widget.winfo_name() == "alarm_on":
                    if state.alarm_data["alarm_on"]:
                        child_widget.configure(bg="green")
                    else:
                        child_widget.configure(bg="red")

        # Plotting Bounds
        t_inner = np.array(statics.coords_inner).T
        t_center = np.array(statics.coords_center).T
        t_outer = np.array(statics.coords_outer).T
        x_inner, y_inner = t_inner
        x_center, y_center = t_center
        x_outer, y_outer = t_outer
        self.ax.plot(x_inner, y_inner, color='orange')
        self.ax.plot(x_center, y_center, color='yellow')
        self.ax.plot(x_outer, y_outer, color='green')

        # Setting View
        self.ax.set_xlim(left=center[0]-graph_width/2, right=center[0]+graph_height/2)
        self.ax.set_ylim(bottom=center[1]-graph_height/2, top=center[1]+graph_height/2)
        self.ax.invert_xaxis()
        self.ax.invert_yaxis()
        
        self.graph.draw()
        logging.debug(f"done output")
            
        
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
                    logging.error("Received something that was not a state object")
                else:
                    self.gui_handler()
            except EOFError as eof:
                logging.debug("End of File")
            
            new_data = True

    
    


if __name__=="__main__":
    app = App()
    app.mainloop()