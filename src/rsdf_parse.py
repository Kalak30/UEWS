import datetime


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
            for i in range(len(words)):
                try:
                    words[i] = int(words[i])
                except ValueError as verr:
                    pass
            # store and get the next line
            last_time = input_time
            input_time = datetime.datetime(words[1], words[2], words[3], words[4], words[5], words[6])

            print("input time", input_time)
            print("last time :", last_time)
            continue

        # if the first instance of PP data, set the input positions
        elif words[0] == 'PP' and words[4] == '11' and first_pp == 1:
            last_position = input_position
            input_position = list(map(float, [words[1], words[2], words[3], words[10], words[11]]))
            first_pp = 0
            print("found pp")
            continue

        # if second or more instance of PP, take average of positions and new PP
        elif words[0] == 'PP' and words[4] == '11' and first_pp == 0:
            new_position = list(map(float, [words[1], words[2], words[3], words[10], words[11]]))

            # combine the new position numbers to get theaverage
            for i in range(len(input_position)):
                input_position[i] = (input_position[i] + new_position[i]) / 2

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
