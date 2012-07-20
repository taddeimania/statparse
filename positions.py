import struct
from stat_map import STAT_MAP

position_offset = {
    'QB': 0,
    'RB': 26,
    'WR': 90,
    'TE': 154,
    'K': 0,
}

class BasePosition(object):

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
        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
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
        )

    def get_condition(self):
        bin_list = []
        for x in range(6034, 6042):
            bin_list.append(bin(ord(self.statfile[x]))[2:])

        for item in bin_list:
            length = len(item)
            if len(item) < 8:
                dif =  8 - length
                item = "0" * dif + item
            print item



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