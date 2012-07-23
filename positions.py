import struct
from stat_map import STAT_MAP
from status_parser import StatusParser

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

injury_dict = {
    "00": "OK",
    "11": "Injured"
}

class BasePosition(object):

    conditions = {}
    injuries = {}
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
        self.rusyds = struct.unpack('H', self.statfile[int(STAT_MAP['rusyds_start'] + base_offset):int(STAT_MAP['rusyds_stop'] + base_offset)])[0]
        if self.rusyds > 1000:
            self.rusyds = struct.unpack('B', self.statfile[STAT_MAP['rusyds_start'] + base_offset])[0]
        self.rustd = struct.unpack('B', self.statfile[STAT_MAP['rustd'] + base_offset])[0]
        self.rec = struct.unpack('B', self.statfile[STAT_MAP['rec'] + rec_offset])[0]
        self.rectd = struct.unpack('B', self.statfile[STAT_MAP['rectd'] + rec_offset])[0]
        self.recyds = struct.unpack('H', self.statfile[int(STAT_MAP['recyds_start'] + rec_offset):int(STAT_MAP['recyds_stop'] + rec_offset)])[0]
        self.kr = struct.unpack('B', self.statfile[STAT_MAP['kr'] + rec_offset])[0]
#        self.kryds = struct.unpack('B', self.statfile[STAT_MAP['kryds'] + rec_offset])[0]
        self.kryds = struct.unpack('H', self.statfile[int(STAT_MAP['kryds_start'] + rec_offset):int(STAT_MAP['kryds_stop'] + rec_offset)])[0]
        self.krtd = struct.unpack('B', self.statfile[STAT_MAP['krtd'] + rec_offset])[0]
        self.pr = struct.unpack('B', statfile[STAT_MAP['pr'] + rec_offset])[0]
        self.prtd = struct.unpack('B', statfile[STAT_MAP['prtd'] + rec_offset])[0]
        self.pryds = struct.unpack('H', self.statfile[int(STAT_MAP['pryds_start'] + rec_offset):int(STAT_MAP['pryds_stop'] + rec_offset)])[0]
        self.xpa = 0
        self.xpm = 0
        self.fga = 0
        self.fgm = 0

        if pos != 'QB':
            self.zero_out_non_qb_stats()
        else:
            self.zero_out_stats_for_qb()

    def get_stats(self):
        return "{}{},1,{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            self.team,
            self.pos,
            self.passatt,
            self.comp,
            self.passtd,
            self.passint,
            self.passyds,
            self.rec,
            self.recyds,
            self.rectd,
            self.rusat,
            self.rusyds,
            self.rustd,
            self.kr,
            self.kryds,
            self.krtd,
            self.pr,
            self.pryds,
            self.prtd,
            #add punt return tds, & kick return tds
            self.xpa,
            self.xpm,
            self.fga,
            self.fgm,
            self.team,
            self.get_player_condition(),
            self.get_other_team(),
            self.get_player_injury(),
        )

    def get_other_team(self):
        for team in self.team_list:
            if self.team != team:
                return team

    def get_player_condition(self):
        if self.pos == "K":
            return "Good"
        return conditions_dict[self.conditions["{}{}".format(self.team, self.pos)]]

    def get_player_injury(self):
        if self.pos == "K":
            return "OK"
        return injury_dict[self.injuries["{}{}".format(self.team, self.pos)]]

    @classmethod
    def get_injuries(cls, file):
        positions = ["QB1", "QB2", "RB1", "RB2", "RB3", "RB4", "WR1", "WR2", "WR3", "WR4", "TE1", "TE2"]
        list_of_statuses = []
        for x in range(6031, 6034):
            list_of_statuses.append(bin(ord(file[x]))[2:])
        for x in range(6292, 6295):
            list_of_statuses.append(bin(ord(file[x]))[2:])

        injuries = StatusParser(list_of_statuses, cls.team_list, positions, file)
        injuries.set_binary_strings()
        injuries.set_condition_on_player_position()
        cls.injuries = injuries.condition_list


    @classmethod
    def get_conditions(cls, file):
        positions = ["QB1", "QB2", "RB1", "RB2", "RB3", "RB4", "WR1", "WR2", "WR3", "WR4", "TE1", "TE2", "C", "LG", "RG", "LT", "RT", "RE", "NT", "LE", "ROLB", "RILB", "LILB", "LOLB", "RCB", "LCB", "FS", "SS"]
        list_of_statuses = []
        for x in range(6034, 6042):
            list_of_statuses.append(bin(ord(file[x]))[2:])
        for x in range(6295, 6303):
            list_of_statuses.append(bin(ord(file[x]))[2:])

#        cls.conditions = status_parser(list_of_statuses, positions, cls.team_list)
        conditions = StatusParser(list_of_statuses, cls.team_list, positions, file)
        conditions.set_binary_strings()
        conditions.set_condition_on_player_position()
        cls.conditions = conditions.condition_list

    def zero_out_stats_for_qb(self):
        self.rec = 0
        self.rectd = 0
        self.recyds = 0
        self.kr = 0
        self.kryds = 0
        self.krtd = 0
        self.pr = 0
        self.pryds = 0
        self.prtd = 0

    def zero_out_non_qb_stats(self):
        self.passatt = 0
        self.comp = 0
        self.passtd = 0
        self.passint = 0
        self.passyds = 0

class QuarterBack(BasePosition):

    def __init__(self, statfile, order, **kwargs):
        self.pos = "QB{}".format(order)
        super(QuarterBack, self).__init__(statfile, order, **kwargs)


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
        self.pr = 0
        self.pryds = 0
        self.krtd = 0
        self.prtd = 0
        self.xpa = struct.unpack('B', statfile[STAT_MAP['xpa'] + offset])[0]
        self.xpm = struct.unpack('B', statfile[STAT_MAP['xpm'] + offset])[0]
        self.fga = struct.unpack('B', statfile[STAT_MAP['fga'] + offset])[0]
        self.fgm = struct.unpack('B', statfile[STAT_MAP['fgm'] + offset])[0]

    def get_stats(self):
        return super(Kicker, self).get_stats()