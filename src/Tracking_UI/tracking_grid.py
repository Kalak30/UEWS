import numpy as np
import logging
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(current_dir))

import statics

# These are important
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas #Places matplotlib plot on tkinter canvas
from matplotlib.figure import Figure    # For creating a figure
from matplotlib.ticker import MultipleLocator

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


sys.path.insert(0, current_dir)

class Canvas(FigureCanvas):
    def __init__(self, parent):
        self.fig = Figure()
        super().__init__(self.fig)
        self.setParent(parent)

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

        self.positions = np.empty(shape=(1,2))
        self.proj_positions = self.positions

    def update_with_state(self, state):
        """Draws the new projected and actual positions on the graph
            Returns the center position
        """
        pos_list_max = 200
        proj_pos_list_max = 20

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
        return new_pos
    
    def new_state(self, state):
        logging.basicConfig(level=logging.DEBUG)
        graph_height=3000
        graph_width=4000
        
        center = np.array((0,0))

        # Clean the graph
        for artist in self.ax.lines + self.ax.collections:
            artist.remove()
        
        if state is not None:
            # Draw new lines or reset position caches
            if state.reset is False:
                center = self.update_with_state(state)
            else:
                self.positions = np.empty((1,2))
                self.proj_positions = self.positions

           

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
        
        self.draw()
        

        

