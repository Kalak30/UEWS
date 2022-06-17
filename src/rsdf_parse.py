import datetime
from function_decorators import *
from tspi import *
import tspi_calc


# Calculates the approximate rolling average given the old average, new value, and the total number of samples
def approx_rolling_avg(old_avg, new_val, number_of_samples):
    return old_avg * (number_of_samples - 1) / number_of_samples + new_val / number_of_samples


# Creating some static variables to make life easier when calculating rolling average
@static("seen_pp", False)
@static("num_pp", 0)
@static("rolling_avg", [0, 0, 0, 0, 0])
def parse_pp(words):
    input_position = list(map(float, [words[1], words[2], words[3], words[10], words[11]]))

    # Calculate average PP position if there are multiple
    if parse_pp.seen_pp:
        if parse_pp.num_pp < 1:
            print("Have seen a PP record but have not parsed it. Returning value of this PP record")
            return input_position

        input_position = [approx_rolling_avg(avg_val, ip_val, parse_pp.num_pp) for avg_val, ip_val in
                          zip(input_position, parse_pp.rolling_avg)]
    else:
        print("found pp")
        parse_pp.seen_pp = True

    parse_pp.num_pp += 1
    parse_pp.rolling_avg = input_position
    return input_position


# Parses an HS record and return the date time it represents
def parse_hs(words):
    try:
        words = [int(word) for word in words]
    except ValueError as verr:
        print(f"Could not convert data to integer: {verr.args}")
    input_time = datetime.datetime(words[1], words[2], words[3], words[4], words[5], words[6])
    return input_time


# Parses through a CS record and determines if a countdown needs to be started
def parse_cs(input_time, last_time, seen_pp):
    # if there was never a PP
    # TODO: ------ADD CODE TO START COUNTDOWN-----
    if seen_pp is False:
        print("no pp")
        # return 3 to show no PP
        return 3
    else:
        return 0


# takes entire message and extracts + updates input position and time
def parse_data(message):
    lines = message.split('\n')
    input_position = list()
    #input_position = {"x_pos": 0, "y_pos": 0, "z_pos": 0, "knots": 0, "heading": 0}
    input_time = datetime.datetime(1, 1, 1, 1, 1)
    seen_pp = False
    for line in lines:

        print(line)
        words = line.split(' ')

        # if blank, go to next line
        if len(words) < 2:
            continue

        # if HS line, get the times, then go to next line
        elif words[0] == "HS":
            input_time = parse_hs(words)
            print("input time", input_time)
            continue

        elif words[0] == 'PP' and words[4] == '11':
            input_position = parse_pp(words)
            seen_pp = True
            continue

        # if CS line, then it is the end of message
        elif words[0] == "CS":
            print("\nend of message")
            parse_cs(input_time, seen_pp)
            # Calculate X and Y speed from knots and heading
            x_speed, y_speed = tspi_calc.get_speed_from_knots(knots=input_position[4], heading=input_position[3])
            return TSPIRecord(x=input_position[0], y=input_position[1], z=input_position[2], x_speed=x_speed,
                              y_speed=y_speed, time=input_time, heading=input_position[3], knots=input_position[4])
        else:
            continue






