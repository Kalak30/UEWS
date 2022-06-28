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


# border boundaries - in yards
# These may be stored in some file in the future, so it is easier for them to change
coords_inner = [(2500, -1200), (2500, 1000), (3100, 1500), (5900, 1500), (8500, 1500), (10000, 1200), (12100, 870),
                (14050, 600), (15560, 1100), (15560, -1530), (9000, -1530), (6800, -830), (5800, -680), (5200, -720),
                (2500, -1200)]
coords_center = [(2500, -1230), (2500, 1220), (3100, 1680), (5900, 1530), (8500, 1590), (10000, 1220), (12100, 930),
                 (14050, 1250), (15560, 1500), (15560, -1680), (9000, -1680), (6800, -900), (5800, -800), (5200, -810),
                 (2500, -1230)]
coords_outer = [(2500, -1400), (2500, 1900), (3100, 1900), (5900, 1600), (8500, 1740), (10000, 1300), (12100, 1150),
                (14050, 1350), (15560, 1500), (15560, -1900), (9000, -1900), (6800, -1020), (5800, -970), (5200, -933),
                (2500, -1400)]

# Path to config file
CONFIG_PATH = '../config/config.yaml'
LOGGER_CONFIG_PATH = './config/logger_config.ini'
