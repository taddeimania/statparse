import struct
from stat_map import STAT_MAP

class BasePosition(object):

    def __init__(self, statfile, base_offset, **kwargs):
        home = kwargs.get('home')
        if not home:
            base_offset += 261
        self.passatt = struct.unpack('B', statfile[STAT_MAP['passatt'] + base_offset])[0]
        self.comp = struct.unpack('B', statfile[STAT_MAP['comp'] + base_offset])[0]
        self.passtd = struct.unpack('B', statfile[STAT_MAP['passtd'] + base_offset])[0]
        self.passint = struct.unpack('B',  statfile[STAT_MAP['passint'] + base_offset])[0]
        self.passyds = struct.unpack('H', statfile[int(STAT_MAP['passyards_start'] + base_offset):int(STAT_MAP['passyards_stop'] + base_offset)])[0]
        self.rusat = struct.unpack('B', statfile[STAT_MAP['rusat'] + base_offset])[0]
        self.rusyds = struct.unpack('B', statfile[STAT_MAP['rusyds'] + base_offset])[0]
        self.rustd = struct.unpack('B', statfile[STAT_MAP['rustd'] + base_offset])[0]

    def print_stats(self):
        print "{},{},{},{},{},{},{},{}".format(
            self.passatt,
            self.comp,
            self.passtd,
            self.passint,
            self.passyds,
            self.rusat,
            self.rusyds,
            self.rustd
        )


class QuarterBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):

        if order == 1:
            base_offset = 0
        else:
            base_offset = 16
        self.pos = "QB{},".format(order)
        super(QuarterBack, self).__init__(statfile, base_offset, **kwargs)

    def print_stats(self):
        print self.pos, "\t",
        super(QuarterBack, self).print_stats()

class RunningBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        if order == 1:
            base_offset = 26
        else:
            base_offset = 26 + (16 * order)

        self.pos = "RB{},".format(order)
        super(RunningBack, self).__init__(statfile, base_offset, **kwargs)

    def print_stats(self):
        print self.pos, "\t",
        super(RunningBack, self).print_stats()