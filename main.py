import struct
from stat_map import STAT_MAP



class BasePosition(object):

    def __init__(self, statfile, base_offset):
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

def get_home_and_away(byte):
    away = ""
    home = ""
    for x in range(3087, 3090):
        home += byte[x]

    for x in range(3119, 3122):
        away += byte[x]

    return home, away

def main():
    f = open("/home/jtaddei/3.nst", "rb")
    byte = f.read()
    home, away = get_home_and_away(byte)
    print "\t\tPASSAT\tCOMP\tPASSTD\tPASSINT\tPASSYDS\t\tRUSAT\tRUSYDS\tRUSTD"
    qb1 = QuarterBack(byte, 1)
    qb1.print_stats()
    for i in range(1, 5):
        rb = RunningBack(byte, i)
        rb.print_stats()

#    rb1 = RunningBack(byte, 1)
#    rb1.print_stats()

if __name__ == "__main__":
    main()