"""Performs a check to determine if an x, y, z position is within the specified boundaries"""

from asyncio.log import logger
import statistics
from statics import coords_inner, coords_outer, coords_center, outer_bound_depth, inner_bound_depth, center_bound_depth, x_outlier, y_outlier, z_outlier, speed_outlier
from shapely.geometry import Point, Polygon
from tspi import TSPIRecord, Vector

inner_poly = Polygon(coords_inner)
center_poly = Polygon(coords_center)
outer_poly = Polygon(coords_outer)



def in_bounds(x, y, z):
    """Determines if a position at x, y, z is within the allowed boundary
    :return bool if point is within allowed boundary"""
    pos = Point(x, y)
    # Z and bounds are negative
    if z < inner_bound_depth.upper:
        return pos.within(inner_poly)
    elif z < center_bound_depth.upper:
        return pos.within(center_poly)

    return pos.within(outer_poly)


#return false is invalid, also check 
def check_vaild_record(pos, knots):
    """Checks if the position and speed of the data is within reason. 
    :return false if outside of reason, true of valid(within reason)"""
    if pos.x < x_outlier.lower or pos.x > x_outlier.upper or pos.y < y_outlier.lower or \
            pos.y > y_outlier.upper or pos.z < z_outlier.lower or pos.z > z_outlier.upper or \
            knots > speed_outlier.upper:
        return False
    return True
    
    #else return true (valid)
    return True

#return false is out of depth, true if ok
def check_in_depth(depth):
    """Checks if depth is below -220 feet. Pretty simple really
    :return true if depth is above -220, false if below -220 feet"""
    if depth < -220:
        return False
    return True

def check_project_boundary(proj_position : Vector):
    return