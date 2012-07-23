class StatusParser(object):

    def __init__(self, list_of_statuses, team_list, positions, file):
        self.statuses = list_of_statuses
        self.team_list = team_list
        self.positions = positions
        self.file = file
        self.binary_strings = []
        self.condition_list = {}

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

    #NOT TDD
    def set_condition_on_player_position(self):
        i, x = 0, 0
        for two_bit in self.binary_strings:
            bit = 0
            bit_interval = 2
            while bit_interval < 9:
                self.condition_list['{}{}'.format(self.team_list[x], self.positions[i])] = (two_bit[bit:bit_interval])
                bit += 2
                bit_interval += 2
                i, x = self.increment_byte_scanner(i, x)

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
        return index == (len(self.positions) - 1)