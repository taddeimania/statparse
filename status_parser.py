def status_parser(list_of_statuses, positions, team_list):
    """ I don't normally comment or doc string but this method is going to confuse the crap
        out of me the instant I walk away from the keyboard.

        The objective of this method is to break each unsigned byte into it's 8 bit binary
        string.  The challenge is that python seems to delete leading zero's so we need
        to add them back in, then we need to break it into 2 bit chunks for analysis.
    """

    bin_list = []

    # find binary strings that have been chopped, add 0's back in
    for item in list_of_statuses:
        length = len(item)
        if len(item) < 8:
            dif =  8 - length
            item = "0" * dif + item
        bin_list.append(item)

    # break each string into 2 bits, create new entry in list for each chunk, these
    # represent player conditions.
    positions = positions
    i = 0
    x = 0
    temp_dict = {}
    for byte in bin_list:
        bit = 0
        bit_interval = 2
        while bit_interval < 9:
            temp_dict['{}{}'.format(team_list[x], positions[i])] = (byte[bit:bit_interval])
            bit += 2
            bit_interval += 2
            if i == (len(positions) - 1):
                i = 0
                if x == 1:
                    break
                x += 1
            else:
                i += 1
    return temp_dict