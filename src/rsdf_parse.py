import datetime


# A decorator to create a static function variable
def static(name, val):
    def decorate(func):
        setattr(func, name, val)
        return func
    return decorate


# Calculates the approximate rolling average given the old average, new value, and the total number of samples
def approx_rolling_avg(old_avg, new_val, number_of_samples):
    return old_avg * (number_of_samples - 1) / number_of_samples + new_val / number_of_samples


# Creating some static variables to make life easier when calculating rolling average
@static("seen_pp", False)
@static("num_pp", 0)
@static("rolling_avg", list())
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
        seen_pp = True

    parse_pp.num_pp += 1
    rolling_avg = input_position
    return input_position


# takes entire message and extracts + updates input position and time
def parse_data(message, input_position, input_time, last_time):
    lines = message.split('\n')
    first_pp = 1
    for line in lines:

        print(line)
        words = line.split(' ')

        # if blank, go to next line
        if len(words) < 2:
            continue

        # if HS line, get the times, then go to next line
        elif words[0] == "HS":
            # store and get the next line
            last_time = input_time

            try:
                words = [int(word) for word in words]
            except ValueError as verr:
                print("Could not convert data to integer")

            input_time = datetime.datetime(words[1], words[2], words[3], words[4], words[5], words[6])
            print("input time", input_time)
            print("last time :", last_time)
            continue

        elif words[0] == 'PP' and words[4] == '11':
            parse_pp(words)
            continue

        # if CS line, then it is th end of message
        elif words[0] == "CS":
            print("\nend of message")

            # if there was never a PP
            # TODO: ------ADD CODE TO START COUNTDOWN-----
            if first_pp == 1:
                print("no pp")

                # set the time back to last time PP was sent
                input_time = last_time

                # return 3 to show no PP
                return 3
            else:
                return 0
        else:
            continue
