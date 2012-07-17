import struct
from stat_map import STAT_MAP

class BasePosition(object):

    def __init__(self, statfile, base_offset, rec_offset, **kwargs):
        home = kwargs.get('home')

        if not home:
            base_offset += 261
            rec_offset += 261

        self.passatt = struct.unpack('B', statfile[STAT_MAP['passatt'] + base_offset])[0]
        self.comp = struct.unpack('B', statfile[STAT_MAP['comp'] + base_offset])[0]
        self.passtd = struct.unpack('B', statfile[STAT_MAP['passtd'] + base_offset])[0]
        self.passint = struct.unpack('B',  statfile[STAT_MAP['passint'] + base_offset])[0]
        self.passyds = struct.unpack('H', statfile[int(STAT_MAP['passyards_start'] + base_offset):int(STAT_MAP['passyards_stop'] + base_offset)])[0]
        self.rusat = struct.unpack('B', statfile[STAT_MAP['rusat'] + base_offset])[0]
        self.rusyds = struct.unpack('B', statfile[STAT_MAP['rusyds'] + base_offset])[0]
        self.rustd = struct.unpack('B', statfile[STAT_MAP['rustd'] + base_offset])[0]
        self.rec = struct.unpack('B', statfile[STAT_MAP['rec'] + rec_offset])[0]
        self.rectd = struct.unpack('B', statfile[STAT_MAP['rectd'] + rec_offset])[0]
        self.recyds = struct.unpack('B', statfile[STAT_MAP['recyds'] + rec_offset])[0]
        self.kr = struct.unpack('B', statfile[STAT_MAP['kr'] + rec_offset])[0]
        self.kryds = struct.unpack('B', statfile[STAT_MAP['kryds'] + rec_offset])[0]

    def print_stats(self):
        print "{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
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
        )


class QuarterBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):

        if order == 1:
            base_offset = 0
        else:
            base_offset = 10
        self.pos = "QB{},".format(order)
        super(QuarterBack, self).__init__(statfile, base_offset, base_offset, **kwargs)
        self.rec = 0
        self.rectd = 0
        self.recyds = 0
        self.kr = 0
        self.kryds = 0

    def print_stats(self):
        print self.pos,
        super(QuarterBack, self).print_stats()

class RunningBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        if order == 1:
            base_offset = 26
            rec_offset = base_offset + 9
        else:
            base_offset = 26 + (16 * order)
            rec_offset = base_offset - 7
        self.pos = "RB{},".format(order)
        super(RunningBack, self).__init__(statfile, base_offset, rec_offset, **kwargs)

    def print_stats(self):
        print self.pos,
        super(RunningBack, self).print_stats()

class WideReceiver(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        if order == 1:
            base_offset = 90
            rec_offset = base_offset + 9
        else:
            base_offset = 90 + (16 * order)
            rec_offset = base_offset - 7
        self.pos = "WR{},".format(order)
        super(WideReceiver, self).__init__(statfile, base_offset, rec_offset, **kwargs)

    def print_stats(self):
        print self.pos,
        super(WideReceiver, self).print_stats()

class TightEnd(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        if order == 1:
            base_offset = 154
            rec_offset = base_offset + 9
        else:
            base_offset = 154 + (16 * order)
            rec_offset = base_offset - 7
        self.pos = "TE{},".format(order)
        super(TightEnd, self).__init__(statfile, base_offset, rec_offset, **kwargs)

    def print_stats(self):
        print self.pos,
        super(TightEnd, self).print_stats()