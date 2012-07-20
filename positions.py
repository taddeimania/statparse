import struct
from stat_map import STAT_MAP

position_offset = {
    'QB': 0,
    'RB': 26,
    'WR': 90,
    'TE': 154,
    'K': 0,
}

conditions_dict = {
    "11": "Excellent",
    "10": "Good",
    "01": "Average",
    "00": "Bad",
}

class BasePosition(object):

    condition_list = {}
    team_list = []
    team = "Not Set"
    pos = "Not Set"

    def __init__(self, statfile, order, **kwargs):
        self.statfile = statfile
        pos = self.pos[:-1] if self.pos != 'K' else 'K'
        home = kwargs.get('home')
        base_offset = position_offset[pos]

        if pos not in ["QB", 'K']:
            if order == 1:
                rec_offset = base_offset + 9
            else:
                base_offset += (16 * order)
                rec_offset = base_offset - 7
        else:
            if order <= 1:
                base_offset = 0
                rec_offset = 0
            else:
                base_offset += 10
                rec_offset = 0

        if not home:
            base_offset += 261
            rec_offset += 261

        self.team = kwargs.get('team')
        self.passatt = struct.unpack('B', self.statfile[STAT_MAP['passatt'] + base_offset])[0]
        self.comp = struct.unpack('B', self.statfile[STAT_MAP['comp'] + base_offset])[0]
        self.passtd = struct.unpack('B', self.statfile[STAT_MAP['passtd'] + base_offset])[0]
        self.passint = struct.unpack('B',  self.statfile[STAT_MAP['passint'] + base_offset])[0]
        self.passyds = struct.unpack('H', self.statfile[int(STAT_MAP['passyards_start'] + base_offset):int(STAT_MAP['passyards_stop'] + base_offset)])[0]
        self.rusat = struct.unpack('B', self.statfile[STAT_MAP['rusat'] + base_offset])[0]
        self.rusyds = struct.unpack('B', self.statfile[STAT_MAP['rusyds'] + base_offset])[0]
        self.rustd = struct.unpack('B', self.statfile[STAT_MAP['rustd'] + base_offset])[0]
        self.rec = struct.unpack('B', self.statfile[STAT_MAP['rec'] + rec_offset])[0]
        self.rectd = struct.unpack('B', self.statfile[STAT_MAP['rectd'] + rec_offset])[0]
        self.recyds = struct.unpack('B', self.statfile[STAT_MAP['recyds'] + rec_offset])[0]
        self.kr = struct.unpack('B', self.statfile[STAT_MAP['kr'] + rec_offset])[0]
        self.kryds = struct.unpack('B', self.statfile[STAT_MAP['kryds'] + rec_offset])[0]
        #self.krtd = struct.unpack('B', statfile[STAT_MAP['kryds'] + rec_offset])[0]
        #self.prtd = struct.unpack('B', statfile[STAT_MAP['kryds'] + rec_offset])[0]
        self.xpa = 0
        self.xpm = 0
        self.fga = 0
        self.fgm = 0

    def get_stats(self):
        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            self.team,
            self.pos,
            self.passatt,
            self.comp,
            self.passtd,
            self.passint,
            self.passyds,
            self.rusat,
            self.rusyds,
            self.rustd,
            self.rec,
            self.rectd,
            self.recyds,
            self.kr,
            self.kryds,
            self.xpa,
            self.xpm,
            self.fga,
            self.fgm,
            self.get_player_condition()
        )

    def get_player_condition(self):
        if self.pos == "K":
            return "Who Cares"
        return conditions_dict[self.condition_list["{}{}".format(self.team, self.pos)]]

    @classmethod
    def get_conditions(cls, file):
        """ I don't normally comment or doc string but this method is going to confuse the crap
            out of me the instant I walk away from the keyboard.

            The objective of this method is to break each unsigned byte into it's 8 bit binary
            string.  The challenge is that python seems to delete leading zero's so we need
            to add them back in, then we need to break it into 2 bit chunks for analysis.
        """
        temp_list = []
        bin_list = []
        # create temp list of variable length binary strings
        for x in range(6034, 6042):
            temp_list.append(bin(ord(file[x]))[2:])
        for x in range(6295, 6303):
            temp_list.append(bin(ord(file[x]))[2:])

        # find binary strings that have been chopped, add 0's back in
        for item in temp_list:
            length = len(item)
            if len(item) < 8:
                dif =  8 - length
                item = "0" * dif + item
            bin_list.append(item)

        # break each string into 2 bits, create new entry in list for each chunk, these
        # represent player conditions.
        # 11 - Excellent
        # 10 - Good
        # 01 - Average
        # 00 - Bad
        positions = ["QB1", "QB2", "RB1", "RB2", "RB3", "RB4", "WR1", "WR2", "WR3", "WR4", "TE1", "TE2", "C", "LG", "RG", "LT", "RT", "RE", "NT", "LE", "ROLB", "RILB", "LILB", "LOLB", "RCB", "LCB", "FS", "SS"]
        i = 0
        x = 0
        team_list = cls.team_list
        for byte in bin_list:
            bit = 0
            bit_interval = 2
            while bit_interval < 9:
                cls.condition_list['{}{}'.format(team_list[x], positions[i])] = (byte[bit:bit_interval])
                bit += 2
                bit_interval += 2
                if i == (len(positions) - 1):
                    i = 0
                    if x == 1:
                        break
                    x += 1
                else:
                    i += 1


class QuarterBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.pos = "QB{}".format(order)
        super(QuarterBack, self).__init__(statfile, order, **kwargs)
        self.zero_out_qb_stats()

    def zero_out_qb_stats(self):
        self.rec = 0
        self.rectd = 0
        self.recyds = 0
        self.kr = 0
        self.kryds = 0

class RunningBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.pos = "RB{}".format(order)
        super(RunningBack, self).__init__(statfile, order, **kwargs)

class WideReceiver(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.pos = "WR{}".format(order)
        super(WideReceiver, self).__init__(statfile, order, **kwargs)

class TightEnd(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.pos = "TE{}".format(order)
        super(TightEnd, self).__init__(statfile, order, **kwargs)

class Kicker(BasePosition):

    def __init__(self, statfile, **kwargs):
        self.pos = "K"
        self.statfile = statfile
        self.team = kwargs.get('team')
        home = kwargs.get('home')
        offset = position_offset[self.pos]

        if not home:
            offset += 261
        self.passatt = 0
        self.comp = 0
        self.passtd = 0
        self.passint = 0
        self.passyds = 0
        self.rusat = 0
        self.rusyds = 0
        self.rustd = 0
        self.rec = 0
        self.rectd = 0
        self.recyds = 0
        self.kr = 0
        self.kryds = 0
        #self.krtd = 0
        #self.prtd = 0
        self.xpa = struct.unpack('B', statfile[STAT_MAP['xpa'] + offset])[0]
        self.xpm = struct.unpack('B', statfile[STAT_MAP['xpm'] + offset])[0]
        self.fga = struct.unpack('B', statfile[STAT_MAP['fga'] + offset])[0]
        self.fgm = struct.unpack('B', statfile[STAT_MAP['fgm'] + offset])[0]

    def get_stats(self):
        return super(Kicker, self).get_stats()