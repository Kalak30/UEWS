"""Performs a check to determine if an x, y, z position is within the specified boundaries"""

from statics import coords_inner, coords_outer, coords_center, outer_bound_depth, inner_bound_depth, center_bound_depth
from shapely.geometry import Point, Polygon

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
