from tspi import *

# Values in feet
x_outlier = {"lower": 7500, "upper": 46680}
y_outlier = {"lower": -6600, "upper": 6600}
z_outlier = {"lower": -600, "upper": 25}
speed_outlier = {"upper": 40}


def invalid_data_alert():
    # TODO: Send message to alert processor.
    return


# Validates if a record
def validate_record(record: TSPIRecord, store: TSPIStore):
    if record.x < x_outlier["lower"] or record.x > x_outlier["upper"] or record.y < y_outlier["lower"] or \
            record.y > y_outlier["upper"] or record.z < z_outlier["lower"] or record.z > z_outlier["upper"] or \
            record.speed > speed_outlier["upper"]:
        invalid_data_alert()
        return

    store.add_record(record)
