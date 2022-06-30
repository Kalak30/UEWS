"""Performs a check to determine if an x, y, z position is within the specified boundaries"""

from asyncio.log import logger
import statistics
from tkinter import INSIDE
from statics import coords_inner, coords_outer, coords_center, outer_bound_depth, inner_bound_depth, center_bound_depth, x_outlier, y_outlier, z_outlier, speed_outlier
from shapely.geometry import Point, Polygon


inner_poly = Polygon(coords_inner)
center_poly = Polygon(coords_center)
outer_poly = Polygon(coords_outer)



def in_bounds(position):
    """Determines if a position at x, y, z is within the allowed boundary
    :return bool if point is within allowed boundary"""
    inside_bounds = False
    pos = Point(position.x, position.y)
    # Z and bounds are negative
    if position.z < inner_bound_depth.upper:
        return pos.within(inner_poly)
    elif position.z < center_bound_depth.upper:
        return pos.within(center_poly)

    return pos.within(outer_poly)

def distance_to_edge(position):
    point = Point(position.x, position.y)
    return inner_poly.exterior.distance(point)

def check_x(x):
    """Returns true if x value is within the allowed bounds. False otherwise
    """
    return x >= x_outlier.lower or x <= x_outlier.upper

def check_y(y):
    """Returns true if y value is within the allowed bounds. False otherwise
    """
    return y >= y_outlier.lower or y <= y_outlier.upper

def check_z(z):
    """Returns true if z value is within the allowed bounds. False otherwise
    """
    return z >= z_outlier.lower or z <= z_outlier.upper

def check_speed(knots):
    """Returns true if speed value is within the allowed bounds. False otherwise
    """
    return knots <= speed_outlier.upper
    
#return false is out of depth, true if ok
def check_in_depth(depth):
    """Checks if depth is below -220 feet. Pretty simple really
    :return true if depth is above -220, false if below -220 feet"""
    if depth < -220:
        return False
    return True