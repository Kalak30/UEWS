"""
Parses different PSK record types and parses a PSK record.
Able to count the amount of PP messages received
"""
import logging
import datetime
import tspi_calc
from function_decorators import static
from tspi import TSPIRecord, Vector


logger = logging.getLogger(__name__)


def approx_rolling_avg(old_avg, new_val, number_of_samples):
    """Calculates the approximate rolling average given the old average, new value, and the total number of samples"""
    return old_avg * (number_of_samples - 1) / number_of_samples + new_val / number_of_samples


@static("seen_pp", False)
@static("num_pp", 0)
@static("rolling_avg", [0, 0, 0, 0, 0])
def parse_pp(words):
    """Parses a PP record based on PSK specification
    :param words the different values in the PP record
    :return the rolling average position (x, y, z, knots, heading) of
            all PP records in the current message"""
    input_position = list(map(float, [words[1], words[2], words[3], words[10], words[11]]))

    # Calculate average PP position if there are multiple
    if parse_pp.seen_pp:
        if parse_pp.num_pp < 1:
            logger.info("Have seen a PP record but have not parsed it. Returning value of this PP record")
            return input_position

        input_position = [approx_rolling_avg(avg_val, ip_val, parse_pp.num_pp) for avg_val, ip_val in
                          zip(input_position, parse_pp.rolling_avg)]
    else:
        print("found pp")
        parse_pp.seen_pp = True

    parse_pp.num_pp += 1
    parse_pp.rolling_avg = input_position
    return input_position


def parse_hs(words):
    """Parses an HS record based on the PSK specifications
    :param words The different values that are stored in an HS record
    :return The time that this record was measured"""
    words.pop(0)
    try:
        words = [int(word) for word in words]
    except ValueError as verr:
        print(f"Could not convert data to integer: {verr.args}")
    input_time = datetime.datetime(words[0], words[1], words[2], words[3], words[4], words[5])
    return input_time


def parse_cs(seen_pp):
    """Parses a CS based on the PSK specifications. The CS (check_sum) record is always the last record sent
    :param seen_pp Has there been a PP record seen in this message
    :return 3 if no PP seen, 0 otherwise? (Needs to change to be something that makes sense)"""
    # if there was never a PP
    # TODO: ------ADD CODE TO START COUNTDOWN-----
    if seen_pp is False:
        print("no pp")
        # return 3 to show no PP
        return 3

    print("reset seen PP for next message")
    parse_pp.seen_pp = False
    return 0


def parse_data(message):
    """Takes entire message and extracts and updates input position and time
    Goes through line by line (record by record) and parses each interesting record (HS, PP, CS)
    :param message An RSDF message
    :return TSPIRecord containing spacial and temporal data contained in the message
            Returns None if no CS Record
    """

    lines = message.split('\n')
    input_position = []
    input_time = datetime.datetime(1, 1, 1, 1, 1)
    seen_pp = False
    for line in lines:

        #print(line)
        words = line.split(' ')

        # if blank, go to next line
        if len(words) < 2:
            continue

        # if HS line, get the times, then go to next line
        if words[0] == "HS":
            input_time = parse_hs(words)
            print("input time", input_time)
            continue

        if words[0] == 'PP' and words[4] == '11':
            input_position = parse_pp(words)
            seen_pp = True
            continue

        # if CS line, then it is the end of message
        if words[0] == "CS":
            print("\nend of message")
            parse_cs(seen_pp)
            # Calculate X and Y speed from knots and heading
            x_speed, y_speed = tspi_calc.get_speed_from_knots(knots=input_position[4], heading=input_position[3])

            pos = Vector(x=input_position[0], y=input_position[1], z=input_position[2])
            speed = Vector(x=x_speed, y=y_speed, z=0)
            new_record = TSPIRecord(pos, speed, time=input_time, heading=input_position[3], knots=input_position[4])

            return new_record

    print("never got a CS")
    return None
