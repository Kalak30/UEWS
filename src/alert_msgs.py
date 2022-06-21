# Gives a common interface to the AlertProcessor. Provides some rudimentary logging as well
from alert_processor import *
import logging

logger = logging.getLogger(__name__)

ap = AlertProcessor(0, 0, 0)


def config_alert_processor(invalid_data_max_count, depth_violation_max_count, proj_pos_violation_max_count):
    global ap
    ap = AlertProcessor(invalid_data_max_count, depth_violation_max_count, proj_pos_violation_max_count)


def invalid_data_alert():
    ap.invalid_data()
    logger.debug(f"Invalid Data Occurrence: {ap.invalid_data_count}")


def depth_violation_alert():
    ap.depth_violation()
    logger.debug(f"Depth Violation Occurrence: {ap.depth_violation_count}")


def bounds_violation_alert():
    ap.bounds_violation_alert()
    logger.debug(f"Projected Position Violation Occurrence: {ap.bounds_violation}")

