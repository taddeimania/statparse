class StatusParser(object):

    def __init__(self, list_of_statuses, team_list, positions, byte):
        self.statuses = list_of_statuses
        self.team_list = team_list
        self.positions = positions
        self.byte = byte
        self.binary_strings = []
        self.condition_list = []

    def set_binary_strings(self):
        for binary_string in self.statuses:
            padded_string = self.pad_binary_string(binary_string)
            self.binary_strings.append(padded_string)

    def pad_binary_string(self, binary_string):
        length = len(binary_string)
        if length < 8:
            dif =  8 - length
            binary_string = "0" * dif + binary_string
        return binary_string

    def set_condition_on_player_position(self):
        pass
#        i, x, bit, bit_interval = (0, 0, 0, 2)
#        while bit_interval < 9:
#            player_key = '{}{}'.format(self.team_list[x], self.positions[i])] = (self.byte[bit:bit_interval]
#            self.condition_list[])
#            bit += 2
#            bit_interval += 2
#            i, x = self.increment_byte_scanner(i, x)


    def increment_byte_scanner(self, i, x):
        if self.last_position(i):
            i = 0
            if x == 1:
                return i, x
            x += 1
        else:
            i += 1
        return i, x

    def last_position(self, index):
        return index == len(self.positions) - 1

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