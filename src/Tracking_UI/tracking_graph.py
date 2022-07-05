import sys
import os
from turtle import position
import numpy as np
import pyqtgraph as pg

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(current_dir))

import statics

class TrackingGraph():
    """ Contains methods and data to graph incoming data"""
    def __init__(self, plot_widget):
        self.plot_widget = plot_widget
        self.positions = np.zeros(shape=(1,2))
        self.proj_positions = self.positions

        self.graph_height=3000
        self.graph_width=4000
        self.center = np.array((0,0))
        self.reset_positions = True

        self.init_graph()

    def init_graph(self):
        """ Test plotting """
        t_inner = np.array(statics.coords_inner).T
        t_center = np.array(statics.coords_center).T
        t_outer = np.array(statics.coords_outer).T
        x_inner, y_inner = t_inner
        x_center, y_center = t_center
        x_outer, y_outer = t_outer
        
        # plot boundaries. clipToView will only render what is in the view
        self.plot_widget.plot(x_inner, y_inner, clipToView=True, pen=pg.mkPen(color="#ff8000"))
        self.plot_widget.plot(x_center, y_center, clipToView=True, pen=pg.mkPen(color="#ffff00"))
        self.plot_widget.plot(x_outer, y_outer, clipToView=True, pen=pg.mkPen(color="#00ff00"))
        
        self.plot_widget.invertX(True)
        self.plot_widget.invertY(True)
        self.plot_widget.showGrid(x=True, y=True)

        # Could make this changable via a button on GUI to allow for graph navigation. Could be cool
        # but not needed
        self.plot_widget.setMouseEnabled(x=False, y=False)

        self.plot_widget.setXRange(0, self.graph_width)
        self.plot_widget.setYRange(0, self.graph_height)

        grid_color = "#0080ff"

        x_axis = self.plot_widget.getAxis('bottom')
        x_axis.setStyle(textFillLimits=[(0,0.6), (4, 0.4)])
        x_axis.setPen(color= grid_color)
        x_axis.setTickSpacing(major=500, minor=50)
        x_axis.setLabel(text="X (feet)")

       

        y_axis = self.plot_widget.getAxis('left')
        y_axis.setStyle(textFillLimits=[(0,0.6), (4, 0.4)])
        y_axis.setPen(color=grid_color)
        y_axis.setTickSpacing(major=200, minor=50)
        y_axis.setLabel(text="Y (feet)")

        


        # Values coming from playing around with GUI. Nothing too rigid
        # Ensures that values at bottom aren't too weird during default size of window
        self.plot_widget.setLimits(minXRange=1000, maxXRange=17000, minYRange=300, maxYRange=5600)
    
    def draw_tracks(self, state):
        """Draws the new projected and actual positions on the graph
            Returns the center position
        """
        pos_list_max = 200
        proj_pos_list_max = 20


        new_record = state.store.records[0]

        new_pos = np.array((new_record.x, new_record.y))
        new_proj_pos = np.array((new_record.proj_x, new_record.proj_y))

        # Need to remove the preinitialized values from numpy to avoid weird drawing issues
        if self.reset_positions:
            self.positions[0,:] = new_pos
            self.proj_positions[0,:] = new_proj_pos
            self.reset_positions = False
        else:
            self.positions = np.vstack((self.positions, new_pos))
            self.proj_positions = np.vstack((self.proj_positions, new_proj_pos))

        # Trim caches
        if len(self.positions) > pos_list_max:
            self.positions = np.delete(self.positions, (0), axis=0)

        if len(self.proj_positions) > proj_pos_list_max:
            self.proj_positions = np.delete(self.proj_positions, (0), axis=0)

        t_position = self.positions.T
        t_proj_pos = self.proj_positions.T
        x_pos, y_pos = t_position
        proj_x, proj_y = t_proj_pos

        if not hasattr(self, "curr_pos_line"):
            self.curr_pos_line = self.plot_widget.plot(x_pos, y_pos, antialias=True, pen=pg.mkPen(color="#008000", width=2))
        else:
            self.curr_pos_line.setData(x_pos, y_pos)

        if not hasattr(self,"proj_pos_line"):
            self.proj_pos_line = self.plot_widget.plot(proj_x, proj_y, antialias=True, pen=pg.mkPen(color="#800000", width=2))
        else:
            self.proj_pos_line.setData(proj_x, proj_y)

        
        return new_pos

    def new_state(self, state):
        """ Redraws the canvas
            Calculates center
        """
        

        # Draw new lines or reset position caches
        if state.reset is False:
            self.center = self.draw_tracks(state)
        else:
            print("reset")
            self.positions = np.zeros((1,2))
            self.proj_positions = self.positions
            self.reset_positions = True

        # Setting View
        self.plot_widget.setXRange(min=self.center[0]-self.graph_width/2, max=self.center[0]+self.graph_width/2)
        self.plot_widget.setYRange(min=self.center[1]-self.graph_height/2, max=self.center[1]+self.graph_height/2)
