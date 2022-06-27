from sre_parse import State
from tkinter import *
from random import randint
import logging
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

new_data = True
state = None
positions = np.zeros(shape=(1,2))
print(positions)
    

def app():

    root = Tk()
    root.config(background="white")
    root.geometry("1000x700")

    lab = Label(root, text="Live Plotting", bg="white").pack()

    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    
    
    ax.grid()
    

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill="both", expand=True)

    def plotter():
        height=3000
        width=4000
        global state
        global new_data
        global positions

        pos_list = []    
        center = 0
        ax.cla()
        ax.grid()

        if state is not None:
            pos_list = np.array([(record.position.x, record.position.y) for record in state.store.records])
            positions = np.vstack((positions, pos_list[0]))
            print(positions)
            t_position = positions.T
            x_pos, y_pos = t_position
            ax.plot(x_pos, y_pos, color='green')
            center = pos_list[0]
            new_data = False

        t_inner = np.array(statics.coords_inner).T
        t_center = np.array(statics.coords_center).T
        t_outer = np.array(statics.coords_outer).T

        x_inner, y_inner = t_inner
        x_center, y_center = t_center
        x_outer, y_outer = t_outer


        ax.plot(x_inner, y_inner, color='yellow')
        ax.plot(x_center, y_center, color='orange')
        ax.plot(x_outer, y_outer, color='red')

        ax.set_xlim(left=center[0]-width/2, right=center[0]+height/2)
        ax.set_ylim(bottom=center[1]-height/2, top=center[1]+height/2)
        

        ax.invert_xaxis()
        ax.invert_yaxis()
        
        

        graph.draw()
            
        
    def gui_handler():
        threading.Thread(target=plotter, daemon=True).start()

    def update_state(listener):
        global state
        global new_data
        conn = listener.accept()
        while True:
            try:
                state = conn.recv()
                gui_handler()
            except EOFError as eof:
                logger.debug("End of File")
            
            print("new data")
            new_data = True

    
    # Listen to backend
    address = ('localhost', 6000)
    listener = Listener(address)

    # Run state update in a different thread so that the GUI is still responsive
    threading.Thread(target=update_state, args=(listener,), daemon=True).start()

    root.mainloop()

if __name__=="__main__":
    app()