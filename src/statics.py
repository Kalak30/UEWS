"""
Contains static data that can be accessed from any module
"""
from collections import namedtuple
Bounds = namedtuple("Bounds", "lower upper")
# Values in feet
x_outlier = Bounds(lower=7500, upper=46680)
y_outlier = Bounds(lower=-6600, upper=6600)
z_outlier = Bounds(lower=-600, upper=25)
speed_outlier = Bounds(lower=0, upper=40)

# Depth in feet under the water
outer_bound_depth = Bounds(lower=-75, upper=0)
center_bound_depth = Bounds(lower=-165, upper=-75)
inner_bound_depth = Bounds(lower=-220, upper=-165)


# border boundaries
# These may be stored in some file in the future, so it is easier for them to change
coords_inner = [(7500, -3600), (7500, 3000), (9300, 4500), (17700, 4500), (25500, 4500), (30000, 3600), (36300, 2610), 
                (42150, 1800), (46680, 3300), (46680, -4590), (27000, -4590), (20400, -2490), (17400, -2040), 
                (15600, -2160), (7500, -3600)]
                
coords_center = [(7500, -3690), (7500, 3660), (9300, 5040), (17700, 4590), (25500, 4770), (30000, 3660), (36300, 2790), 
                 (42150, 3750), (46680, 4500), (46680, -5040), (27000, -5040), (20400, -2700), (17400, -2400), 
                 (15600, -2430), (7500, -3690)]
coords_outer = [(7500, -4200), (7500, 5700), (9300, 5700), (17700, 4800), (25500, 5220), (30000, 3900), (36300, 3450), 
                (42150, 4050), (46680, 4500), (46680, -5700), (27000, -5700), (20400, -3060), (17400, -2910), 
                (15600, -2799), (7500, -4200)]

# Path to config file
CONFIG_PATH = '../config/config.yaml'
LOGGER_CONFIG_PATH = './config/logger_config.ini'
